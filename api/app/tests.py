from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from .models import Post


class PostReadOnlyViewsetTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Post.objects.create(title='title1', body='body1',
                            author='1', is_published=True, published_date=timezone.now())
        Post.objects.create(title='title2', body='body2',
                            author='2', is_published=False)

    def test_get_list(self):
        api_client = APIClient()
        resp = api_client.get('/app/posts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        posts = Post.objects.all()
        for key in ['id', 'title', 'body', 'is_published']:
            with self.subTest(key=key):
                self.assertEqual(resp.data[0][key],
                                 posts[0].__dict__[key])

    def test_get_detail(self):
        api_client = APIClient()
        resp = api_client.get('/app/posts/1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        posts = Post.objects.all()
        for key in ['id', 'title', 'body', 'is_published']:
            with self.subTest(key=key):
                self.assertEqual(resp.data[key],
                                 posts[0].__dict__[key])
        resp = api_client.get('app/post/2/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
