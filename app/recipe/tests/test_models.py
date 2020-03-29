from django.test import TestCase
from django.contrib.auth import get_user_model

from recipe.models import Tag


class RecipeModelTests(TestCase):

    def new_user(self, email="test@test.com", password="testpass123"):
        """Helper function to create test user"""
        return get_user_model().objects.create_user(
            email=email,
            password=password,
        )

    def test_tag_string(self):
        """Test string representation for a tag"""
        test_user = self.new_user()
        tag = Tag.objects.create(
            user=test_user,
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)
