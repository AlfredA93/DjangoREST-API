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
        # Make a request to posts url, create a post
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


class PostDetailTests(APITestCase):
    """Post Detail View Tests"""
    def setUp(self):
        """Data used for Tests """
        # Set up Users
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass2')
        # Create posts by each user
        Post.objects.create(
            owner=adam, title='Adam on Holiday', content='Holiday Description'
        )
        Post.objects.create(
            owner=brian, title='Brian at work', content='Workday Description'
        )

    def test_can_retrieve_post_using_valid_id(self):
        """Test retrieve post"""
        # View the post detail
        response = self.client.get('/posts/1/')
        # Test Title data
        self.assertEqual(response.data['title'], 'Adam on Holiday')
        # Test status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        """Retrieve data with id"""
        response = self.client.get('/posts/123456/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        """User can update post"""
        # User Login
        self.client.login(username='adam', password='pass')
        # Request post to update with data
        response = self.client.put('/posts/1/', {'title': 'Adam on Holiday in Portugal'})
        post = Post.objects.filter(pk=1).first()
        # Test the title is the same
        self.assertEqual(post.title, 'Adam on Holiday in Portugal')
        # Test the status code of update request
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_users_post(self):
        """User cant update other users posts"""
        # User Login
        self.client.login(username='adam', password='pass')
        # Request post to update with data
        response = self.client.put('/posts/2/', {'title': 'Adam editting Brians post'})
        # Test the status code of update request
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
