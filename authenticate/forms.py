# for customizing signin and registration forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username - required for sign in'}), max_length=30)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AuthorizeUser(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))