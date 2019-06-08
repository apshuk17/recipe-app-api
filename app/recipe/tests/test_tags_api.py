from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    '''Test the publicly available tags API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required for retrieving tags'''

        res = self.client.get(TAGS_URL)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)


class PrivateTagsApiTests(TestCase):
    '''Test authorized user tags API'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test123@gmail.com',
            password='test@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_tags(self):
        '''Test retrieving tags'''

        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(serializer.data, res.data)

    def test_tags_limited_to_user(self):
        '''Test that tags returned are for authenticated user'''

        user_non_auth = get_user_model().objects.create_user(
            email='testOther123@gmail.com',
            password='test@123'
        )

        Tag.objects.create(user=user_non_auth, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Spicy')
        res = self.client.get(TAGS_URL)

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(1, len(res.data))
        self.assertEqual(res.data[0].get('name'), tag.name)
