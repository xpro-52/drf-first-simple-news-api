from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from . import views

app_name = 'jwt_auth'

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh')
]

