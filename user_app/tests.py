"""#user_app\tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_app.models import Profile

class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@example.com',
            'firstname': 'Test',
            'lastname': 'User',
            'phone': '1234567890',
            'date_of_birth': '2000-01-01',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  # Assuming the view renders the same template on success
        self.assertTrue(response.context['success'])
        self.assertContains(response, 'Created successfully')

    def test_register_view_post_invalid_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'wrongpassword',
            'email': 'invalidemail',
            'firstname': '',
            'lastname': '',
            'phone': '',
            'date_of_birth': 'invalid-date',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        self.assertContains(response, 'Please fill in complete information')

    # Add more test cases as needed for edge cases and validation scenarios

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_post_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), data)
        
        # Assert that it redirects to the login page due to invalid credentials
        self.assertRedirects(response, '/login/')

"""