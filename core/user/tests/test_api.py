import json

from django.urls import reverse
from django.contrib.auth import authenticate
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
        )
        cls.user.set_password('password')
        cls.user.save()
        cls.token = Token.objects.create(user=cls.user)

    def test_login_wrong_username(self):
        """
        Test login when user by a given username is not in Database
        """
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

    def test_login_wrong_password(self):
        """
        Test login with wrong password
        """
        url = reverse('user:user_login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertIsNone(response.data.get('token'))

    def test_login_success(self):
        """
        Test successfull login request
        """
        url = reverse('user:user_login')
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('token'), self.token.key)


class UserRegisterTests(APITestCase):
    def test_register_no_password(self):
        """
        Test user registration without password
        """
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
        """
        Test user registration without username
        """
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
        """
        Test user registration with invalid email address
        """
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

    def test_register_username_max_length(self):
        """
        Test username returns error when max_length exceeds 150
        """
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
        """
        Test successfull registration
        """
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


class UserProfileTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
            username='testuser',
            email='email@mail.com',
            first_name='first name',
            last_name='last_name'
        )
        cls.user.set_password('test_password')
        cls.token = Token.objects.create(
            user=cls.user
        )

    def test_get_user_profile_not_authenticated(self):
        """
        Test GET user profile method without authentication
        """
        url = reverse('user:user_profile')
        response = self.client.get(url)

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            str(response.data.get('detail')),
            'Authentication credentials were not provided.'
        )

    def test_patch_user_profile_not_authenticated(self):
        """
        Test PATCH user profile method without authentication
        """
        url = reverse('user:user_profile')
        data = {
            'username': 'new_username',
            'email': 'new_email@mail.com',
            'first_name': 'new name',
            'last_name': 'new last name'
        }
        response = self.client.patch(url, data)

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            str(response.data.get('detail')),
            'Authentication credentials were not provided.'
        )

    def test_get_user_profile_success(self):
        """
        Test GET user profile data is successfull
        """
        self.client.force_authenticate(self.user)
        url = reverse('user:user_profile')
        response = self.client.get(url)
        expected_data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'avatar': None
        }

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)
        self.assertIsNone(response.data.get('password'))

    def test_patch_user_profile_success(self):
        """
        Test PATCH user profile is successfull
        """
        self.client.force_authenticate(self.user)
        url = reverse('user:user_profile')
        data = {
            'username': 'new_username',
            'email': 'new_email@mail.com',
            'first_name': 'new name',
            'last_name': 'new last name'
        }
        response = self.client.patch(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        updated_user = User.objects.get(id=self.user.id)
        expected_data = {
            'username': updated_user.username,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'avatar': None
        }

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertTrue(all([
            updated_user.username == 'new_username',
            updated_user.first_name == 'new name',
            updated_user.last_name == 'new last name',
            updated_user.email == 'new_email@mail.com'
        ]))
        self.assertIsNone(response.data.get('password'))

    def test_patch_change_single_data(self):
        """
        Test PATHC user profile to change single field (username)
        """
        self.client.force_authenticate(self.user)
        url = reverse('user:user_profile')
        data = {
            'username': 'new_username',
        }
        response = self.client.patch(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        updated_user = User.objects.get(id=self.user.id)
        expected_data = {
            'username': updated_user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'avatar': None
        }

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertTrue(all([
            updated_user.username == 'new_username',
            updated_user.first_name == self.user.first_name,
            updated_user.last_name == self.user.last_name,
            updated_user.email == self.user.email
        ]))
        self.assertIsNone(response.data.get('password'))

    def test_change_user_password(self):
        """
        Test change user password
        """
        self.client.force_authenticate(self.user)
        url = reverse('user:user_profile')
        data = {
            'password': 'new_password',
        }
        response = self.client.patch(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        new_token = Token.objects.get(user=self.user).key
        expected_data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'avatar': None,
            'token': new_token
        }
        user = authenticate(
            username=self.user.username,
            password='new_password'
        )

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertNotEqual(self.token.key, new_token)
        self.assertTrue(user)
        self.assertIsNone(response.data.get('password'))
