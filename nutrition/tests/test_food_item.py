from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import FoodItem

class CreateFoodItem(APITestCase):
    def setUp(self):
        self.email = "test@email.com"
        self.user = User.objects.create_user(username=self.email, email=self.email)

    def tearDown(self):
        User.objects.all().delete()
        FoodItem.objects.all().delete()

    def test_missing_macronutrient(self):
        name = "oatmeal"
        fat = 12
        carb = 36

        url = '/nutri/test/'
        factory = APIRequestFactory()
        view = controller.FoodItemController.as_view()
        request = factory.post(
            url,
            json.dumps({
                "name": name,
                "fat": fat,
                "carb": carb
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400)

    def test_negative_macronutrient(self):
        name = "oatmeal"
        protein = -8
        fat = 12
        carb = 36

        url = '/nutri/test/'
        factory = APIRequestFactory()
        view = controller.FoodItemController.as_view()
        request = factory.post(
            url,
            json.dumps({
                "name": name,
                "protein": protein,
                "fat": fat,
                "carb": carb
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400)

    def test_missing_name(self):
        protein = 9
        fat = 12
        carb = 36

        url = '/nutri/test/'
        factory = APIRequestFactory()
        view = controller.FoodItemController.as_view()
        request = factory.post(
            url,
            json.dumps({
                "fat": fat,
                "carb": carb
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400)
    
    def test_create_food_item(self):
        name = "oatmeal"
        protein = 9
        fat = 12
        carb = 36

        url = '/nutri/fooditem/'
        factory = APIRequestFactory()
        view = controller.FoodItemController.as_view()
        request = factory.post(
            url,
            json.dumps({
                "name": name,
                "protein": protein,
                "fat": fat,
                "carb": carb
            }),
            content_type='application/json'
        )
        force_authenticate(request, user=self.user)
        response = view(request)

        fooditem_response = response.data['fooditem']
        fooditem = FoodItem.objects.get(pk=fooditem_response['id'])

        # Assert HTTP Response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(fooditem_response["name"], name)
        self.assertEqual(fooditem_response["protein"], protein)
        self.assertEqual(fooditem_response["fat"], fat)
        self.assertEqual(fooditem_response["carb"], carb)

        # Assert Object created in DB
        self.assertEqual(fooditem.user, self.user)
        self.assertEqual(fooditem.name, name)
        self.assertEqual(fooditem.protein, protein)
        self.assertEqual(fooditem.fat, fat)
        self.assertEqual(fooditem.carb, carb)