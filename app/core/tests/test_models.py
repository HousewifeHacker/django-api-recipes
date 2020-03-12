from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):


    def new_user(self, email="test@test.com", password="testpass123"):
        """Helper function to create new user"""
        return get_user_model().objects.create_user(
            email=email,
            password=password,
        )


    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@test.com"
        password = "testpass123"
        user = self.new_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_is_normalized(self):
        """Test creating a user normalizes the email"""
        email = "test@TEst.com"
        user = self.new_user(email=email)

        expected_email = "test@test.com"
        self.assertEqual(user.email, expected_email)


    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            self.new_user(email=None)


    def test_new_superuser_successful(self):
        """Test new superuser can be created and is staff"""
        email = "test@test.com"
        password = "testpass123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
