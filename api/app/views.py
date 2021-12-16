from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import PostSerializer, PostProSerializer
from .models import Post


class PostReadOnlyViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        self.queryset = queryset
        return queryset


class PostProViewset(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostProSerializer