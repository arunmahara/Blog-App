from distutils.command.upload import upload
from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    datetime= models.DateTimeField(auto_now = True)
    picture = models.ImageField(upload_to = 'pics', blank=True)