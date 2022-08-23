from django.contrib import admin
from .models import Blog, Connection

# Register your models here.
@admin.register(Blog) 
# show data with fields form in admin panel
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'title', 'desc', 'datetime', 'picture')

@admin.register(Connection) 
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id','person', 'followers')