from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:create_token')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


def get_user(**params):
    """Helper function to get user object"""
    return get_user_model().objects.get(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def assert_no_user(self, email):
        """Helper function to assert user with email does not exist"""
        user_exists_bool = get_user_model().objects.filter(
            email=email
        ).exists()
        self.assertFalse(user_exists_bool)

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Create user API with valid payload is successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    def test_creating_user_that_exists(self):
        """Test creating user with duplicate email from api fails"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'name',
        }
        create_user(**payload)
        payload2 = {
            'email': 'test@test.com',
            'password': 'testpass2',
            'name': 'name2',
        }
        res = self.client.post(CREATE_USER_URL, payload2)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password less than 5 characters fails to create user"""
        payload = {
            'email': 'test@test.com',
            'password': 'pw12',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_no_user(payload['email'])

    def test_create_user_requires_password(self):
        """Test that create user api fails without password"""
        payload = {
            'email': 'test@test.com',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_no_user(payload['email'])

    def test_create_user_requires_name(self):
        """Test that create user api fails without name"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_no_user(payload['email'])

    def test_create_token_valid(self):
        """With valid user, create token"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.com', password='testpass')
        payload = {'email': 'test@test.com', 'password': 'wrong'}
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assert_no_user(payload['email'])
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_requires_password(self):
        """Test that token is not created if payload is missing password"""
        create_user(email='test@test.com', password='testpass')
        payload = {'email': 'test@test.com'}
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_requires_email(self):
        """Test that token is not created if payload is missing email"""
        create_user(email='test@test.com', password='testpass')
        payload = {'passowrd': 'testpass'}
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
