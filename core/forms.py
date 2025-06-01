from django import forms
from .models import BucketListItem, CompletedItem

class BucketListItemForm(forms.ModelForm):
    class Meta:
        model = BucketListItem
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 4}),
        }

class CompletionForm(forms.ModelForm):
    class Meta:
        model = CompletedItem
        fields = ['description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }