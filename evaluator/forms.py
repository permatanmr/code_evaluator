from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control w-80', 'placeholder': 'Enter your full name'})
    )
    
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control w-80', 'placeholder': 'Enter your username'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control w-80', 'placeholder': 'Enter your email'})
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control w-80', 'placeholder': 'Enter your password'})
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control w-80', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']
