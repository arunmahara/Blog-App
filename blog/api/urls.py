from importlib import import_module
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

#Creating Router Object
router = DefaultRouter()

# Register BlogModelViewSet and UserModelViewSet with Router
router.register('userApi', views.UserModelViewSet, basename='user')
router.register('blogApi', views.BlogModelViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls))
]