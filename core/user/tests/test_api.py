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
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertIsNone(response.data.get('token'))


class UserRegisterTests(APITestCase):
    def test_register_no_password(self):
        url = reverse('user:user_register')
        data = {
            'username': 'username',
        }
        response = self.client.post(url, data)
        error_msg = str(response.data.get('password')[0])

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_msg, 'This field is required.')
        self.assertEqual(len(response.data), 1)

    def test_register_no_username(self):
        url = reverse('user:user_register')
        data = {
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        error_msg = str(response.data.get('username')[0])

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_msg, 'This field is required.')
        self.assertEqual(len(response.data), 1)

    def test_register_bad_email(self):
        url = reverse('user:user_register')
        data = {
            'username': 'username',
            'email': 'some bad email',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        error_msg = str(response.data.get('email')[0])

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_msg, 'Enter a valid email address.')

    def test_register_fields_max_length(self):
        long_string = 's' * 151
        url = reverse('user:user_register')
        data = {
            'username': long_string,
            'email': 'test@mail.com',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': 'testpassword'
        }

        response = self.client.post(url, data)
        error_msg = str(response.data.get('username')[0])

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            error_msg,
            'Ensure this field has no more than 150 characters.'
        )

    def test_register_user_success(self):
        url = reverse('user:user_register')
        data = {
            'username': 'username',
            'email': 'test@mail.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)

        qs = User.objects.filter(username='username')
        user = qs.first()
        user_exists = qs.exists()
        self.assertTrue(user_exists)

        expected_response = {
            'user_id': user.id
        }

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)
