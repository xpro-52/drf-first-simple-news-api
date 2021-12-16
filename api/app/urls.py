from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('posts', views.PostReadOnlyViewset, basename='posts')
router.register('posts-pro', views.PostProViewset, basename='posts-pro')

urlpatterns = [
    path('', include(router.urls))
]
