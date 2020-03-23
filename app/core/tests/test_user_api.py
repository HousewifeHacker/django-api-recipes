from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


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
        """Creating using with a valid payload with create user API is successful"""
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
        """Creates a user then asserts creating duplicate user with create api fails"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password shorter than 5 characters fails to create new user"""
        payload = {
            'email': 'test@test.com',
            'password': 'pw12',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_no_user(payload['email']) 

    def test_create_user_requires_password(self):
        """Test that create user api fails without password"""
        payload = {
            'email': 'test@test.com',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_no_user(payload['email'])

