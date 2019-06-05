from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''Test the users API(public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successfully(self):
        '''Test creating user with valid payload is successful'''
        payload = {
            'email': 'abc@gmail.com',
            'password': 'isAwesome',
            'name': 'Apoorva'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''Test creating a user already exists fail'''
        payload = {
            'email': 'abc@gmail.com',
            'password': 'isAwesome',
            'name': 'Apoorva'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_password_too_short(self):
        '''Test password must be at least 5 characters long'''
        payload = {
            'email': 'abc@gmail.com',
            'password': 'isA',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        user_exists = get_user_model().objects.filter(
            email=payload.get('email')
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''Test that a token is created for the user'''
        payload = {
            'email': 'abc@gmail.com',
            'password': 'isAwesome',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(status.HTTP_200_OK, res.status_code)

    def test_create_token_invalid_credentials(self):
        '''Test that token is not created when invalid credentials are given'''
        create_user(email='abc@gmail.com', password='abc@123', name='Lorem')
        payload = {
            'email': 'abc@gmail.com',
            'password': 'wrong@123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_create_no_token_user_not_exist(self):
        '''Test that no token is created if user does not exist'''
        payload = {
            'email': 'abc@gmail.com',
            'password': 'abc@123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_create_missing_field(self):
        '''Test that email and password are required'''
        res = self.client.post(TOKEN_URL,
            {'email': 'abc@gmail.com', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)