from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Blog
from .forms import SignupForm, LoginForm

# Create your views here.
def signupUser(request):
    if request.method =='POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            # user = fm.save()
            # login (request, user)     
            messages.success(request, 'Signup Successful')
            return redirect('/')      
    else:
        fm = SignupForm()
    return render(request, 'signup.html', {'form':fm})


def loginUser(request):
    if request.method == 'POST':
        fm = LoginForm(request = request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages. success(request, 'Login successful')
                return redirect('blog')
    else:
        fm = LoginForm()
    return render(request, 'login.html', {'form':fm})    


def blog (request):
    blog = Blog.objects.all()    
    return render(request, 'blog.html', {'blogs':blog})