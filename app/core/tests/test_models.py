from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_success(self):
        '''Test creating a new user with an email is successful'''

        email = 'apshuk14@gmail.com'
        password = 'apoorva@17'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test the email for a new user is  normalized'''
        email = 'apshuk12@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email, password='loremipsum'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_with_invalid_email(self):
        '''Test creating new users with invalid email'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'loremipsum')

    def test_create_new_super_user(self):
        '''Test creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'apshuk14@gmail.com',
            'apoorva@17'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
