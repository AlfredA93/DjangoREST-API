"""Tests for Posts Model"""
# pylint: disable=E1101
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post


class PostListViewTests(APITestCase):
    """Post List Tests"""
    def setUp(self):
        """Create User"""
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        """Test List"""
        # Get the User
        adam = User.objects.get(username='adam')
        # Create a post with the user
        Post.objects.create(owner=adam, title='a title')
        # Test the response when requesting an url. Instead of '.get', can also use .post .put
        response = self.client.get('/posts/')
        # Initiate the test
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        """Logged In Post Creation Test"""
        # Login as Adam
        self.client.login(username='adam', password='pass')
        # Make a request to posts url
        response = self.client.post('/posts/', {'title': 'a title'})
        # Count all the posts in 'posts/'
        count = Post.objects.count()
        # Test if it is 1
        self.assertEqual(count, 1)
        # Test if response code is 201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_logged_in_to_post(self):
        """Test User must be logged in to post"""
        response = self.client.post('/posts/', {'title': 'title2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
