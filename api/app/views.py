from rest_framework import request, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import PostSerializer
from .models import Post


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(is_published=True)
        self.queryset = queryset
        return queryset
