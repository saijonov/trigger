from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bucket-list/', views.BucketListView.as_view(), name='bucket-list'),
    path('item/<int:pk>/', views.BucketItemDetailView.as_view(), name='item-detail'),
    path('suggest/', views.suggest_item, name='suggest-item'),
    path('item/<int:pk>/complete/', views.complete_item, name='complete-item'),
    path('completion/<int:pk>/', views.CompletionDetailView.as_view(), name='completion-detail'),
    path('completion/<int:pk>/delete/', views.DeleteCompletionView.as_view(), name='completion-delete'),
    path('user/<int:user_id>/completions/', views.UserCompletionsView.as_view(), name='user-completions'),
    
    # Admin paths - changed from admin/ to staff/ to avoid conflict
    path('staff/pending/', views.PendingItemsView.as_view(), name='pending-items'),
    path('staff/item/<int:pk>/approve/', views.approve_item, name='approve-item'),
    path('staff/item/<int:pk>/reject/', views.reject_item, name='reject-item'),
]