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
                    messages.success(request, 'Login Successful')
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
    blog = Blog.objects.all().order_by('-datetime')    
    return render(request, 'home.html', {'blogs':blog})

@login_required(login_url='/')
def myblogs(request):
    blog = Blog.objects.filter(user=request.user).order_by('-datetime')
    return render(request, 'myblogs.html', {'blogs':blog}) 

@login_required(login_url='/')
def post(request):
    if request.method == 'POST':
        fm = PostForm(request.POST, request.FILES)
        if fm.is_valid():
            instance = fm.save(commit = False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Blog Posted')
            return redirect('home')
    else:
        fm = PostForm()
    return render(request,'post.html',{'form':fm})


@login_required(login_url='/')
def profile(request):
    return render(request, 'profile.html')
 
@login_required(login_url='/')
def profileChange(request):
    if request.method =='POST':
        fm =ProfileChangeForm(instance=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Update Successful')
            return redirect('profile')
    else:
        fm = ProfileChangeForm(instance=request.user)
    return render (request, 'profilechange.html', {'form':fm}) 

@login_required(login_url='/')
def deleteBlog(request, id):
    if request.method == 'POST':
        blog = Blog.objects.get(pk=id)
        blog.delete()
        messages.success(request, 'Blog Deleted')
        return redirect('myblogs')
