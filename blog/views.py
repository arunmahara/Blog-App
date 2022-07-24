from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Blog
from .forms import SignupForm

# Create your views here.
def index(request):
    blog = Blog.objects.all()
    return render(request, 'index.html', {'blogs':blog})

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
    return render(request, 'signup.html',{'form':fm})


def loginUser(request):
    return render(request, 'login.html')    