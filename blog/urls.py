from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('signup', views.signupUser, name='signup'),
    path('home', views.home, name='home'),
    path('myblogs', views.myblogs, name='myblogs'),
    # path('post', views.post, name='post'),
    path('logout', views.logoutUser, name='logout')
]
