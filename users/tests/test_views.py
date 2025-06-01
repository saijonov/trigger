from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')

    def test_register_view_get(self):
        """Test register view GET request"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post(self):
        """Test register view POST request"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        """Test register view POST request with invalid data"""
        data = {
            'username': 'newuser',
            'email': 'invalid_email',
            'password1': 'newpass123',
            'password2': 'different_password'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on same page
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """Test login view"""
        # Test GET request
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        # Test successful login
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

        # Test invalid login
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on same page

    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_profile_view_authenticated(self):
        """Test profile view when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_profile_view_unauthenticated(self):
        """Test profile view when not authenticated"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('login', response.url) 