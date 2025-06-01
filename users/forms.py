from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Simplify form by removing help text
        for field in self.fields:
            self.fields[field].help_text = None
            self.fields[field].widget.attrs.update({'class': 'w-full px-3 py-2 border rounded-lg'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 4}),
            'profile_pic': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }