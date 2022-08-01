from importlib import import_module
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

#Creating Router Object
router = DefaultRouter()

# Register BlogModelViewSet and UserModelViewSet with Router
router.register('userApi', views.UserModelViewSet, basename='user')
router.register('blogApi', views.BlogModelViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify')
    
]