from unittest.case import skip
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status

from .models import Post


USER = get_user_model()

class PostViewsetTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = USER.objects.create_user(username='tester', email='a@a.com', password='testpass')

        Post.objects.create(title='title1', body='body1',
                            author=user, is_published=True, published_date=timezone.now())
        Post.objects.create(title='title2', body='body2',
                            author=user, is_published=False)
        Post.objects.create(title='title3', body='body3',
                            author=user, is_published=True, published_date=timezone.now())

    def test_get_list(self):
        resp = APIClient().get('/app/posts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_get_detail(self):
        api_client = APIClient()
        resp = api_client.get('/app/posts/1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], Post.objects.order_by('id')[0].title)
        resp = api_client.get('app/post/2/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def _get_authenticated_api_client(self):
        api_client = APIClient()
        data = {'username': 'tester',
                'password': 'testpass'}
        resp = api_client.post('/auth/token/', data)
        api_client.credentials(HTTP_AUTHORIZATION='Bearer '+resp.data['access'])
        return api_client

    def test_get_list_authenticated(self):
        api_client = self._get_authenticated_api_client()
        resp = api_client.get('/app/posts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 3)  # include not public post

    def test_get_detail_authenticated(self):
        api_client = self._get_authenticated_api_client()
        resp = api_client.get('/app/posts/2/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data['is_published'])
        self.assertEqual(resp.data['title'], Post.objects.order_by('id')[1].title)

    def test_create_authenticated(self):
        api_client = self._get_authenticated_api_client()
        data = {
            'title': 'title4',
            'body': 'body4',
            'is_published': True,
            'published_date': timezone.now(),
            'author': 'tester',
        }
        resp: Response = api_client.post('/app/posts/', data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 4)

    def test_update_authenticated(self):
        api_client = self._get_authenticated_api_client()
        data = {
            'title': 'title updated3',
            'body': 'body3',
            'author': 'tester'
        }
        resp: Response = api_client.put('/app/posts/3/', data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.first().title, data['title'])

    def test_delete_authenticated(self):
        api_client = self._get_authenticated_api_client()
        resp: Response = api_client.delete('/app/posts/1/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 2)
    