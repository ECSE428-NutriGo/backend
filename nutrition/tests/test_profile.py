from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile.models import Profile

class TestSignupUser(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.password = "comPlexPasSword942"

    def tearDown(self):
        User.objects.all().delete()

    def test_user_registration(self):
        user_count = len(User.objects.all())

        client = APIClient()
        response = client.post('/rest-auth/registration/', 
            {'email': self.email, 'username': self.email, 'password1': self.password, 'password2': self.password},
            format='json')

        self.key = response.data['key']
        self.assertTrue("key" in response.data) # Assert that an authentication token is received
        self.assertEqual(len(User.objects.all()), user_count+1) # Assert a new user in the database
        self.assertEqual(response.status_code, 201) # Assert a successful status code

    def test_invalid_email_and_valid_password(self):
        user_count = len(User.objects.all())

        bad_email = "1234"

        client = APIClient()
        response = client.post('/rest-auth/registration/', 
            {'email': bad_email, 'username': bad_email, 'password1': self.password, 'password2': self.password},
            format='json')

        self.assertEqual(str(response.data['email'][0]), 'Enter a valid email address.') # Assert error message is sent
        self.assertEqual(len(User.objects.all()), user_count) # Assert a new user in the database
        self.assertEqual(response.status_code, 400) # Assert a successful status code

    def test_valid_email_and_invalid_password(self):
        user_count = len(User.objects.all())

        bad_pass = "1234"

        client = APIClient()
        response = client.post('/rest-auth/registration/', 
            {'email': self.email, 'username': self.email, 'password1': bad_pass, 'password2': bad_pass},
            format='json')

        # Assert bad password response messages are sent
        self.assertEqual(str(response.data['password1'][0]), 'This password is too short. It must contain at least 8 characters.')
        self.assertEqual(str(response.data['password1'][1]), 'This password is too common.')
        self.assertEqual(str(response.data['password1'][2]), 'This password is entirely numeric.')
        self.assertEqual(len(User.objects.all()), user_count) # Assert a new user in the database
        self.assertEqual(response.status_code, 400) # Assert a successful status code

    def test_invalid_email_and_invalid_password(self):
        user_count = len(User.objects.all())

        bad_email = "1234"
        bad_pass = "1234"

        client = APIClient()
        response = client.post('/rest-auth/registration/', 
            {'email': bad_email, 'username': bad_email, 'password1': bad_pass, 'password2': bad_pass},
            format='json')

        self.assertEqual(str(response.data['email'][0]), 'Enter a valid email address.') # Assert error message is sent

        # Assert bad password response messages are sent
        self.assertEqual(str(response.data['password1'][0]), 'This password is too short. It must contain at least 8 characters.')
        self.assertEqual(str(response.data['password1'][1]), 'This password is too common.')
        self.assertEqual(str(response.data['password1'][2]), 'This password is entirely numeric.')
        self.assertEqual(len(User.objects.all()), user_count) # Assert a new user in the database
        self.assertEqual(response.status_code, 400) # Assert a successful status code


class TestLoginUser(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.password = "comPlexPasSword942"
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)

    def tearDown(self):
        User.objects.all().delete()

    def test_user_login(self):
        user_count = len(User.objects.all())

        client = APIClient()
        response = client.post('/rest-auth/login/', 
            {'username': self.email, 'password': self.password},
            format='json')

        self.key = response.data['key']
        self.assertTrue("key" in response.data) # Assert that an authentication token is received
        self.assertEqual(len(User.objects.all()), user_count) # Assert no new user created in the database
        self.assertEqual(response.status_code, 200) # Assert a successful status code

    def test_user_login_invalid_email(self):
        user_count = len(User.objects.all())

        client = APIClient()
        response = client.post('/rest-auth/login/', 
            {'username': 'invalidemail', 'password': self.password},
            format='json')

        self.assertTrue("key" not in response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Unable to log in with provided credentials.')
        self.assertEqual(response.status_code, 400) # Assert a successful status code

    def test_user_login_wrong_password(self):
        user_count = len(User.objects.all())

        client = APIClient()
        response = client.post('/rest-auth/login/', 
            {'username': self.email, 'password': 'wrong.passwordxx'},
            format='json')

        self.assertTrue("key" not in response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Unable to log in with provided credentials.')
        self.assertEqual(response.status_code, 400) # Assert a successful status code

class TestUpdateUserMacros(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.password = "comPlexPasSword942"
        self.curr_protein = 15
        self.curr_fat = 20
        self.curr_carb = 30
        self.new_protein = 20
        self.new_fat = 15
        self.new_carb = 40

        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.user.profile.protein_target = self.curr_protein
        self.user.profile.fat_target = self.curr_fat
        self.user.profile.carb_target = self.curr_carb

    def tearDown(self):
        User.objects.all().delete()

    def test_edit_user_macros(self):
        token, created = Token.objects.get_or_create(user=self.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.put('/rest-auth/user/', 
            {"protein_target": self.new_protein,
            "carb_target": self.new_carb,
            "fat_target": self.new_fat, 
            'username': self.email},
            format='json')

        profile = User.objects.get(pk=response.data['pk']).profile

        # Assert profile targets have been update appropriately
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.protein_target, self.new_protein)
        self.assertEqual(profile.fat_target, self.new_fat)
        self.assertEqual(profile.carb_target, self.new_carb)

    def test_edit_only_protein_target(self):
        token, created = Token.objects.get_or_create(user=self.user)

        profile = User.objects.get(pk=self.user.pk).profile

        profile.protein_target = self.curr_protein
        profile.fat_target = self.curr_fat
        profile.carb_target = self.curr_carb
        profile.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.put('/rest-auth/user/', 
            {"protein_target": self.new_protein,
            'username': self.email},
            format='json')

        profile = User.objects.get(pk=response.data['pk']).profile

        # Assert profile targets have been update appropriately
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.protein_target, self.new_protein)
        self.assertEqual(profile.fat_target, self.curr_fat)
        self.assertEqual(profile.carb_target, self.curr_carb)

    def test_negative_macros(self):
        token, created = Token.objects.get_or_create(user=self.user)

        profile = User.objects.get(pk=self.user.pk).profile

        profile.protein_target = self.curr_protein
        profile.fat_target = self.curr_fat
        profile.carb_target = self.curr_carb
        profile.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.put('/rest-auth/user/', 
            {"protein_target": -5,
            "carb_target": -5,
            "fat_target": -5, 
            'username': self.email},
            format='json')

        # Assert profile targets have been update appropriately
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.protein_target, self.curr_protein)
        self.assertEqual(profile.fat_target, self.curr_fat)
        self.assertEqual(profile.carb_target, self.curr_carb)

class TestProfileCreation(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.password = "comPlexPasSword942"

    def tearDown(self):
        User.objects.all().delete()
    
    def test_create_profile(self):

        self.user = User.objects.create_user(username=self.email, email=self.email)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.user.profile, profile)