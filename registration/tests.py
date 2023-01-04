from django.urls import reverse
from registration.models import AuthUser as User
from rest_framework import status
from base.utils import BaseAPITestCase


class UserTests(BaseAPITestCase):
    def setUp(self):
        self.authorize_requests()

    def test_register_user(self):
        """
        Ensure we can register a new user
        """
        url = reverse('register-users')

        data = {
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Bob",
            "last_name": "Evans"
        }

        response = self.client.post(path=url, data=data, format='json')

        registered_user = response.data["data"]

        # Make sure we have two users in the database
        self.assertEqual(User.objects.count(), 2)

        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Additionally, we want to return the email upon successful creation.
        self.assertEqual(registered_user['email'], registered_user['email'])
        self.assertFalse('password' in registered_user)
        self.assertEqual(len(registered_user["accounts"]), 1)

    def test_create_user_with_no_email(self):
        url = reverse('register-users')
        data = {
            'email': '',
            'password': 'foobar'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_preexisting_email(self):
        url = reverse('register-users')
        data = {
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_list_users(self):
        url = reverse('list-users')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_get_access_token(self):
        url = reverse('token_obtain_pair')
        data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
