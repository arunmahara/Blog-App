from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')  #user as FK
    title = models.CharField(max_length=200)
    desc = models.TextField()
    datetime= models.DateTimeField(auto_now = True)
    picture = models.ImageField(upload_to = 'pics', blank=True)
    likes = models.ManyToManyField(User, related_name='blog_like')

    def total_likes(self):
        return self.likes.count()