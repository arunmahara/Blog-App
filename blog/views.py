from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Blog, Connection
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, PostForm, ProfileChangeForm
from django.urls import reverse

# Create your views here.
# user sign up
def signupUser(request):
    if not request.user.is_authenticated:   # prevents authenticated user from signup
        if request.method =='POST':
            fm = SignupForm(request.POST)
            if fm.is_valid():
                user = fm.save()
                login (request, user, backend='django.contrib.auth.backends.ModelBackend')  #auto login after signup   
                messages.success(request, 'Signup Successful')
                return redirect('home')      
        else:
            fm = SignupForm()
        return render(request, 'signup.html', {'form':fm})
    else:
        return redirect('home')

# user authentication & login
def loginUser(request):
    if not request.user.is_authenticated:   # prevents authenticated user from login
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

# logout user
def logoutUser(request):
    logout(request)
    return redirect('/')

# shows all the post on home page
# restrictions for anonymous user using decorators
@login_required(login_url='/') 
def home (request):
    blog = Blog.objects.all().order_by('-datetime')   
    return render(request, 'home.html', {'blogs':blog})

# shows all the blogs of requested user(own blogs)
@login_required(login_url='/')
def myblogs(request):
    blog = Blog.objects.filter(user=request.user).order_by('-datetime')
    return render(request, 'myblogs.html', {'blogs':blog}) 

# for posting blogs
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

# user profile
@login_required(login_url='/')
def profile(request):
    return render(request, 'profile.html')

# updates user profile
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

# deletes blog
@login_required(login_url='/')
def deleteBlog(request, id):
    if request.method == 'POST':
        blog = Blog.objects.get(pk=id)
        blog.delete()
        messages.success(request, 'Blog Deleted')
        return redirect('myblogs')

# updates blog  
@login_required(login_url='/')
def updateBlog(request, id):
    if request.method == 'POST':
        blog = Blog.objects.get(pk=id)
        blg = PostForm(request.POST, request.FILES, instance=blog)
        if blg.is_valid():
            blg.save()
            messages.success(request, 'Post Updated')
            return redirect('home')
    else:
        blog = Blog.objects.get(pk=id)
        blg = PostForm(instance = blog)
    return render (request, 'post.html', {'form':blg}) 
    
# search requested query 
@login_required(login_url='/')
def search(request):
    if request.method == 'POST':
        query = request.POST['search']
        if len(query) > 50:
            blog =  Blog.objects.none()
        else:
            blogtitle  = Blog.objects.filter(title__icontains=query)  #search query on database
            blogdesc  = Blog.objects.filter(desc__icontains=query)
            blog = blogtitle.union(blogdesc)
            # blog = list(chain(bloguserfirst, blogtitle, blogdesc))  # another way of combining queryset     
        context = {'blogs': blog, 'query':query}
        return render (request, 'search.html', context) 
    else:
        return HttpResponseNotFound('Page Not Found')

# like blog
def likeBlog(request, id):
    blog = get_object_or_404(Blog, pk=id) 
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return HttpResponseRedirect(reverse('home'))

# shows all user in connect template
def connectUser(request):
    users = User.objects.all()
    following = Connection.objects.filter(followers=request.user)   # following users
    following_user =[]
    for each in following:
        following_user.append(each.person)
    context = {'users':users, 'following_user':following_user}
    return render(request, 'connect.html', context)

#follow/unfollow user
def followUnfollow(request, id):
    user = User.objects.get(pk=id)
    connection = Connection.objects.filter(person=user).filter(followers=request.user)     # object where person is specific user and follower is current user
    if request.method == 'POST':
        if connection:                           
            connection.delete() #unfollow
        else:
            Connection.objects.create(person=user, followers=request.user)  #follow
    return redirect('connect')