from cProfile import label
from dataclasses import fields
from logging import PlaceHolder
from django import forms
import django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from requests import request
from .models import Blog
from django.contrib.auth.forms import PasswordResetForm   # password_reset_form to override

# signup form
class SignupForm(UserCreationForm):

    def clean_email(self):   # for unique email 
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    # setting attributes to model form
    first_name = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}))
    last_name =forms.CharField(max_length=30, widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=100, widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1= forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2= forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

# login form
class LoginForm(AuthenticationForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

# blog post form
class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'desc', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Title'}),
            'desc': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Description'}),
        }

# profile update form
class ProfileChangeForm(UserChangeForm):
    password = None  #excludes password
    def clean_email(self):   # for unique email excluding own email
        user_email = self.instance.email
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and user_email.lower() != email.lower():
            raise forms.ValidationError("Email already exists")
        return email
    
    first_name = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}))
    last_name =forms.CharField(max_length=30, widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=100, widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
            }


# check email for password_reset
class EmailValidationOnForgotPassword(PasswordResetForm):  
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
        return email