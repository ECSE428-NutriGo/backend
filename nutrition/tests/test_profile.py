from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile.models import Profile

class TestUserCreation(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.password = "comPlexPasSword942"

    def tearDown(self):
        User.objects.all().delete()

    def test_create_user(self):
        user_count = len(User.objects.all())

        client = APIClient()
        response = client.post('/rest-auth/registration/', 
            {'email': self.email, 'username': self.email, 'password1': self.password, 'password2': self.password},
            format='json')

        self.key = response.data['key']
        self.assertTrue("key" in response.data)
        self.assertEqual(len(User.objects.all()), user_count+1)
        self.assertEqual(response.status_code, 201)

    def test_edit_user(self):
        user = User.objects.create_user(self.email, email=self.email, password=self.password)
        token, created = Token.objects.get_or_create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.put('/rest-auth/user/', 
            {"protein_target": 190,
            "carb_target": 300,
            "fat_target": 130, 
            'username': self.email},
            format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['protein_target'], '190')
    
    def test_create_profile(self):

        self.user = User.objects.create_user(username=self.email, email=self.email)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.user.profile, profile)