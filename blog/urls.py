from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('signup', views.signupUser, name='signup'),
    path('home', views.home, name='home'),
    path('myblogs', views.myblogs, name='myblogs'),
    path('post', views.post, name='post'),
    path('profile', views.profile, name='profile'),
    # path('profileChange', views.profileChange, name='profileChange'),
    path('logout', views.logoutUser, name='logout')
]
