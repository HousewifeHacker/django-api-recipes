from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Create super user and normal user. Log in as superuser"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="testSuperUser@test.com",
            password="testPass123",
        )
        self.client.force_login(self.admin_user)
        self.normal_user = get_user_model().objects.create_user(
            email="testuser@test.com",
            password="testPass123",
            name="testUser Name",
        )

    def test_users_listed(self):
        """Test user name and email are in admin user list response"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.normal_user.email)
        self.assertContains(res, self.normal_user.name)

    def test_user_page_change(self):
        """Test ok status of user edit page"""
        url = reverse('admin:core_user_change', args=[self.normal_user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_page_add(self):
        """Test ok status of user add page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
