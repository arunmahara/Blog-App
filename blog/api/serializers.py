import values
from blog.models import Blog
from django.contrib.auth.models import User
from rest_framework import serializers

# user serializer
class UserSerializer(serializers.ModelSerializer):
    blog = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='blog-detail')
    class Meta:
        model  = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','last_login', 'is_active', 'is_staff', 'password', 'blog']
        read_only_fields = ['last_login', 'is_active', 'is_staff']  #read only items
    
    # user data validation
    def create(self, validated_data):  
        user = User.objects.create_user(**validated_data)
        return user

    # for unique email 
    def validate_email(self, value):   
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

# blog serializer
class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Blog
        fields = ['id', 'user', 'title', 'desc', 'datetime', 'picture', 'url']

