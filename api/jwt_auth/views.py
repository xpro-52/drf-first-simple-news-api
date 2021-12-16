from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer

# USER = get_user_model

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer