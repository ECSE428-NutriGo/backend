from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import FoodItem, Meal

class CreateMeal(APITestCase):
    def setUp(self):
        self.email = "test@email.com"
        self.name1 = 'item 1'
        self.name2 = 'item 2'
        self.name3 = 'item 3'
        self.protein1 = 10
        self.protein2 = 20
        self.protein3 = 30
        self.fat1 = 6
        self.fat2 = 7
        self.fat3 = 8
        self.carb1 = 22
        self.carb2 = 33
        self.carb3 = 44

        self.user = User.objects.create_user(username=self.email, email=self.email)
        FoodItem.objects.create(user=self.user, protein=self.protein1, carb=self.carb1, fat=self.fat1, name=self.name1)
        FoodItem.objects.create(user=self.user, protein=self.protein2, carb=self.carb2, fat=self.fat2, name=self.name2)
        FoodItem.objects.create(user=self.user, protein=self.protein3, carb=self.carb3, fat=self.fat3, name=self.name3)

    def tearDown(self):
        User.objects.all().delete()
        FoodItem.objects.all().delete()
        Meal.objects.all().delete()

    def test_create_meal_no_food_items(self):
        name = "meal without food items"

        url = '/nutri/meal/'
        factory = APIRequestFactory()
        view = controller.MealController.as_view()
        request = factory.post(
            url,
            json.dumps({
                "name": "meal without food items",
                "protein": self.protein1,
                "fat": self.fat1,
                "carb": self.carb1
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        meal_response = response.data['meal']
        meal = Meal.objects.get(pk=meal_response['id'])

        # Assert HTTP Response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meal_response["name"], name)
        self.assertEqual(meal_response["fooditems"], [])
        self.assertEqual(meal_response["protein"], self.protein1)
        self.assertEqual(meal_response["fat"], self.fat1)
        self.assertEqual(meal_response["carb"], self.carb1)

        # Assert Object created in DB
        self.assertEqual(meal.protein, self.protein1)
        self.assertEqual(meal.fat, self.fat1)
        self.assertEqual(meal.carb, self.carb1)
        self.assertEqual(len(meal.fooditems.all()), 0)

    def test_create_meal(self):
        name = "meal 1"
        fooditems = [1, 2, 3]

        url = '/nutri/meal/'
        factory = APIRequestFactory()
        view = controller.MealController.as_view()
        request = factory.post(
            url,
            json.dumps({
                "fooditems": fooditems,
                "name": name
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        meal_response = response.data['meal']
        meal = Meal.objects.get(pk=meal_response['id'])

        # Assert HTTP Response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meal_response["name"], name)
        self.assertEqual(meal_response["fooditems"], fooditems)
        self.assertEqual(meal_response["protein"], self.protein1 + self.protein2 + self.protein3)
        self.assertEqual(meal_response["fat"], self.fat1 + self.fat2 + self.fat3)
        self.assertEqual(meal_response["carb"], self.carb1 + self.carb2 + self.carb3)

        # Assert Object created in DB
        self.assertEqual(meal.protein, self.protein1 + self.protein2 + self.protein3)
        self.assertEqual(meal.fat, self.fat1 + self.fat2 + self.fat3)
        self.assertEqual(meal.carb, self.carb1 + self.carb2 + self.carb3)
        self.assertEqual(len(meal.fooditems.all()), 3)
