from django import views
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailValidationOnForgotPassword  #email validation class for password_reset 

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('signup', views.signupUser, name='signup'),
    path('home', views.home, name='home'),
    path('myblogs', views.myblogs, name='myblogs'),
    path('post', views.post, name='post'),
    path('profile', views.profile, name='profile'),
    path('profileChange', views.profileChange, name='profileChange'),
    path('deleteBlog/<int:id>/', views.deleteBlog, name='deleteBlog'),
    path('updateBlog/<int:id>/', views.updateBlog, name='updateBlog'),
    path('search', views.search, name='search'),
    path('logout', views.logoutUser, name='logout'),
    path('likeblog/<int:id>/', views.likeBlog, name='likeblog'),

    path('password_reset/',auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),name='password_reset'),  #password_reset_form
    path('', include('django.contrib.auth.urls')),   #reset password with email

    path('oauth/', include('social_django.urls', namespace='social')),  # social auth

]
