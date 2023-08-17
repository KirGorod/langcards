from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from user.models import User


class UserLoginTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@mail.com',
            password='password'
        )
        cls.token = Token.objects.create(user=cls.user)

    def test_login_wrong_username(self):
        url = reverse('user:user_login')
        data = {
            'username': 'wronguser',
            'password': 'password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertIsNone(response.data.get('token'))
