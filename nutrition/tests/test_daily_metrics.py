from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem

class CreateDailyMetrics(APITestCase):

    def setUp(self):
        self.email = "testA@email.com"
        self.user = User.objects.create_user(username=self.email, email=self.email)

        self.name = 'meal 1'
        self.protein = 10
        self.fat = 20
        self.carb = 30

        Meal.objects.create(user = self.user, protein = self.protein, fat = self.fat, carb = self.carb)
        meal = Meal.objects.get(pk=1)
        MealEntry.objects.create(user = self.user, meal = meal, timestamp = '2020-02-10')
        MealEntry.objects.create(user = self.user, meal = meal)

    def tearDown(self):
        User.objects.all().delete()
        MealEntry.objects.all().delete()
        Meal.objects.all().delete()

    def test_get_daily_metrics_no_meals(self):

        user = User.objects.create_user(username='new@user.com', email='new@user.com')

        url = '/nutri/daily/'
        factory = APIRequestFactory()
        view = controller.DailyMetrics.as_view()
        request = factory.get(url)
        
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['num_meals'], 0)
        self.assertEqual(response.data['protein'], 0)
        self.assertEqual(response.data['carb'], 0)
        self.assertEqual(response.data['fat'], 0)

    def test_get_daily_metrics_one_meal(self):

        url = '/nutri/daily/'
        factory = APIRequestFactory()
        view = controller.DailyMetrics.as_view()
        request = factory.get(url)
        
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['num_meals'], 1)
        self.assertEqual(response.data['protein'], self.protein)
        self.assertEqual(response.data['carb'], self.carb)
        self.assertEqual(response.data['fat'], self.fat)
    
    def test_get_daily_metrics_multiple_meals(self):
        
        meal = Meal.objects.get(pk=1)

        MealEntry.objects.create(user = self.user, meal = meal)
        url = '/nutri/daily/'
        factory = APIRequestFactory()
        view = controller.DailyMetrics.as_view()
        request = factory.get(url)
        
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['num_meals'], 2)
        self.assertEqual(response.data['protein'], self.protein + self.protein)
        self.assertEqual(response.data['carb'], self.carb + self.carb)
        self.assertEqual(response.data['fat'], self.fat + self.fat)


