from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json
from rest_framework.test import APIClient

from django.test import Client
from django.contrib.auth.models import User
from nutrition import controller
from profile.models import Profile

class CreateUser(APITestCase):

    def setUp(self):
        self.email = "test@email.com"
        self.password = "password"
        self.protein_target = 300
        self.carb_target = 200
        self.fat_target = 100

       self.user = User.objects.create_superuser(username=self.email, email=self.email, password=self.password)
    
    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete() #i think it would do this when it deletes all the users because of the FK

    def test_create_profile(self):

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.user.profile, profile)

    
    
