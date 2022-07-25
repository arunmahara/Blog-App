from cProfile import label
from dataclasses import fields
from enum import unique
from logging import PlaceHolder
from tkinter import Widget
from django import forms
import django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Blog

class SignupForm(UserCreationForm):

    def clean_email(self):   # for unique email 
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
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


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

