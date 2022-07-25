from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Blog
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, PostForm, ProfileChangeForm

# Create your views here.
def signupUser(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            fm = SignupForm(request.POST)
            if fm.is_valid():
                user = fm.save()
                login (request, user)     
                messages.success(request, 'Signup Successful')
                return redirect('home')      
        else:
            fm = SignupForm()
        return render(request, 'signup.html', {'form':fm})
    else:
        return redirect('home')


def loginUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request = request, data = request.POST)
            if fm.is_valid():
                username = fm.cleaned_data['username']
                password = fm.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages. success(request, 'Login successful')
                    return redirect('home')
        else:
            fm = LoginForm()
        return render(request, 'login.html', {'form':fm})
    else:
        return redirect('home')   

def logoutUser(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def home (request):
    blog = Blog.objects.all()    
    return render(request, 'home.html', {'blogs':blog})

@login_required(login_url='/')
def myblogs(request):
    blog = Blog.objects.filter(user=request.user)
    return render(request, 'myblogs.html', {'blogs':blog}) 

@login_required(login_url='/')
def post(request):
    if request.method == 'POST':
        fm = PostForm(request.POST, request.FILES)
        if fm.is_valid():
            instance = fm.save(commit = False)
            instance.user = request.user
            instance.save()
            return redirect('home')
    else:
        fm = PostForm()
    return render(request,'post.html',{'form':fm})

