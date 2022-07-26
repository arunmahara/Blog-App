from django.contrib import admin
from .models import Blog

# Register your models here.
@admin.register(Blog) 
# show data with fields form in admin panel
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'title', 'desc', 'datetime', 'picture')