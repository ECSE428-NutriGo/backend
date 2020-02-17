from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem


class CreateMealEntry(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.user = User.objects.create_user(username=self.email, email=self.email)

        self.name = 'meal 1'
        self.protein = 10
        self.fat = 20
        self.carb = 30

        #to make a meal entry we need a meal
        Meal.objects.create(user = self.user, protein = self.protein, fat = self.fat, carb = self.carb)

    def tearDown(self):
        User.objects.all().delete()
        MealEntry.objects.all().delete()
        Meal.objects.all().delete()
        

    def test_create_meal_entry(self):
        name = "meal entry"
        meal_id = 1

        url = '/nutri/mealentry/'
        factory = APIRequestFactory()
        view = controller.MealEntryController.as_view()
        request = factory.post(
            url, 
            json.dumps({
                "meal": meal_id
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        meal_entry_response = response.data['mealentry']
        meal_entry = MealEntry.objects.get(pk=meal_entry_response['id'])

        # Assert HTTP Response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meal_entry_response["meal"], meal_id)

        # Assert Object created in DB
        self.assertEqual(meal_entry.id, meal_id)

    def test_create_meal_entry_with_timestamp(self):
        name = "meal entry"
        timestamp = '2020-02-04T03:02:24Z'
        meal_id = 1

        url = '/nutri/mealentry/'
        factory = APIRequestFactory()
        view = controller.MealEntryController.as_view()
        request = factory.post(
            url, 
            json.dumps({
                "meal": meal_id,
                "timestamp": timestamp
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        meal_entry_response = response.data['mealentry']
        meal_entry = MealEntry.objects.get(pk=meal_entry_response['id'])

        # Assert HTTP Response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meal_entry_response["meal"], meal_id)

        # Assert Object created in DB
        self.assertEqual(meal_entry.id, meal_id)
        self.assertEqual(str(meal_entry.timestamp), '2020-02-04 03:02:24+00:00')

    def test_create_meal_entry_no_meal(self):

        url = '/nutri/mealentry/'
        factory = APIRequestFactory()
        view = controller.MealEntryController.as_view()
        request = factory.post(
            url, 
            json.dumps({
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        # Assert HTTP Response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Error: no meal provided')

