from datetime import datetime
from blog.models import Blog
from django.contrib.auth.models import User
from .serializers import BlogSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# user model viewset
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #search and order filter
    filter_backends=[SearchFilter, OrderingFilter]
    search_fields=['username', 'first_name', 'last_name']
    ordering_fields=['id', 'first_name']

    # authentication_classes = [JWTAuthentication]  # locally setting simple JWTAuthentication
    # permission_classes=[IsAuthenticated]   # locally setting permission classes
  

# blog model viewset
class BlogModelViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    #search and order filter
    filter_backends=[SearchFilter, OrderingFilter]
    search_fields=['title', 'desc']
    ordering_fields=['id', 'user', 'title', 'datetime']

    # authentication_classes = [JWTAuthentication]
    # permission_classes=[IsAuthenticated]
  