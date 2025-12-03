from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile, AccountabilityPartner, UserSettings

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.onboarding_completed)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_login(self):
        User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        login_data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_logout(self):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.onboarding_url = reverse('onboarding')

    def test_onboarding_completion(self):
        onboarding_data = {
            'primary_goal': 'Learn programming',
            'motivation_why': 'Career growth',
            'daily_time_commitment': 60,
            'has_tried_before': True,
            'previous_attempts': 'Tried online courses'
        }
        response = self.client.post(self.onboarding_url, onboarding_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.onboarding_completed)

class AccountabilityPartnerTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', username='user1', password='pass123')
        self.user2 = User.objects.create_user(email='user2@example.com', username='user2', password='pass123')
        self.client.force_authenticate(user=self.user1)
        self.add_partner_url = reverse('add-partner')

    def test_add_accountability_partner(self):
        partner_data = {'partner_email': 'user2@example.com'}
        response = self.client.post(self.add_partner_url, partner_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AccountabilityPartner.objects.filter(user=self.user1, partner=self.user2).exists())

    def test_cannot_add_self_as_partner(self):
        partner_data = {'partner_email': 'user1@example.com'}
        response = self.client.post(self.add_partner_url, partner_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserSettingsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        # UserSettings is created automatically by signal, so no need to create manually
        self.client.force_authenticate(user=self.user)
        self.settings_url = reverse('user-settings')

    def test_get_user_settings(self):
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['theme'], 'light')

    def test_update_user_settings(self):
        update_data = {'theme': 'dark', 'language': 'es'}
        response = self.client.patch(self.settings_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.settings.refresh_from_db()
        self.assertEqual(self.user.settings.theme, 'dark')