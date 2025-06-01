from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.urls import reverse_lazy
from .models import BucketListItem, CompletedItem, ItemView
from .forms import BucketListItemForm, CompletionForm

def home(request):
    """Home page view"""
    # Get approved bucket list items
    bucket_items = BucketListItem.objects.filter(is_approved=True)[:8]
    
    # Get recent completions
    recent_completions = CompletedItem.objects.all().order_by('-date_completed')[:6]
    
    # Get popular completions (most viewed)
    popular_completions = CompletedItem.objects.annotate(
        view_count=Count('item_views')
    ).order_by('-view_count')[:6]
    
    context = {
        'bucket_items': bucket_items,
        'recent_completions': recent_completions,
        'popular_completions': popular_completions,
    }
    return render(request, 'core/home.html', context)

class BucketListView(ListView):
    """View for browsing all bucket list items"""
    model = BucketListItem
    template_name = 'core/bucket_list.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = BucketListItem.objects.filter(is_approved=True)
        
        # Filter by completion status if specified
        status = self.request.GET.get('status')
        if status == 'completed' and self.request.user.is_authenticated:
            completed_ids = self.request.user.completed_items.values_list('bucket_item_id', flat=True)
            queryset = queryset.filter(id__in=completed_ids)
        elif status == 'uncompleted' and self.request.user.is_authenticated:
            completed_ids = self.request.user.completed_items.values_list('bucket_item_id', flat=True)
            queryset = queryset.exclude(id__in=completed_ids)
            
        return queryset

class BucketItemDetailView(DetailView):
    """View for a single bucket list item"""
    model = BucketListItem
    template_name = 'core/item_detail.html'
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get completions for this item
        context['completions'] = self.object.completions.all()
        
        # Check if user has completed this item
        if self.request.user.is_authenticated:
            context['user_completed'] = self.object.completions.filter(user=self.request.user).exists()
            
        return context

@login_required
def suggest_item(request):
    """View for suggesting a new bucket list item"""
    if request.method == 'POST':
        form = BucketListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, "Your bucket list item has been submitted for approval!")
            return redirect('home')
    else:
        form = BucketListItemForm()
    
    return render(request, 'core/suggest_item.html', {'form': form})

@login_required
def complete_item(request, pk):
    """View for completing a bucket list item"""
    item = get_object_or_404(BucketListItem, pk=pk, is_approved=True)
    
    # Check if user has already completed this item
    if CompletedItem.objects.filter(user=request.user, bucket_item=item).exists():
        messages.warning(request, "You've already completed this bucket list item!")
        return redirect('item-detail', pk=pk)
    
    if request.method == 'POST':
        form = CompletionForm(request.POST, request.FILES)
        if form.is_valid():
            completion = form.save(commit=False)
            completion.user = request.user
            completion.bucket_item = item
            completion.save()
            messages.success(request, f"Congratulations on completing '{item.title}'!")
            return redirect('completion-detail', pk=completion.pk)
    else:
        form = CompletionForm()
    
    return render(request, 'core/complete_item.html', {'form': form, 'item': item})

class CompletionDetailView(DetailView):
    """View for a completed item"""
    model = CompletedItem
    template_name = 'core/completion_detail.html'
    context_object_name = 'completion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Record a view if user hasn't viewed this completion yet
        session_key = f'viewed_completion_{self.object.pk}'
        if not self.request.session.get(session_key, False):
            ItemView.objects.create(
                item=self.object,
                user=self.request.user if self.request.user.is_authenticated else None,
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
            self.request.session[session_key] = True
            # Save the session explicitly for test environment
            self.request.session.save()
            
        # Get view count
        context['view_count'] = ItemView.objects.filter(item=self.object).count()
        
        return context

class UserCompletionsView(LoginRequiredMixin, ListView):
    """View for a user's completed items"""
    model = CompletedItem
    template_name = 'core/user_completions.html'
    context_object_name = 'completions'
    paginate_by = 12
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return CompletedItem.objects.filter(user__id=user_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['profile_user'] = get_object_or_404(User, id=user_id)
        return context

# Admin views
class PendingItemsView(UserPassesTestMixin, ListView):
    """View for admin to see pending bucket list items"""
    model = BucketListItem
    template_name = 'core/admin/pending_items.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        print("\nPendingItemsView.get_queryset() called")  # Debug print
        return BucketListItem.objects.filter(is_approved=False)
    
    def test_func(self):
        print(f"\nPendingItemsView.test_func() called. User: {self.request.user}, is_staff: {self.request.user.is_staff}")  # Debug print
        return self.request.user.is_staff

    def handle_no_permission(self):
        print("\nPendingItemsView.handle_no_permission() called")  # Debug print
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home')

@login_required
def approve_item(request, pk):
    """View for approving a bucket list item"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to do that.")
        return redirect('home')
        
    item = get_object_or_404(BucketListItem, pk=pk)
    item.is_approved = True
    item.save()
    
    messages.success(request, f"The bucket list item '{item.title}' has been approved!")
    return redirect('pending-items')

@login_required
def reject_item(request, pk):
    """View for rejecting a bucket list item"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to do that.")
        return redirect('home')
        
    item = get_object_or_404(BucketListItem, pk=pk)
    item.delete()
    
    messages.success(request, "The bucket list item has been rejected and deleted.")
    return redirect('pending-items')

class DeleteCompletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a completion"""
    model = CompletedItem
    template_name = 'core/completion_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('user-completions', kwargs={'user_id': self.object.user.id})
    
    def test_func(self):
        completion = self.get_object()
        # Check if user is the owner or staff
        return self.request.user == completion.user or self.request.user.is_staff
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "You don't have permission to delete this completion.")
        return redirect('completion-detail', pk=self.kwargs.get('pk'))