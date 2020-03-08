from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem


initial_name="name1"
initial_protein=1
initial_fat=1
initial_carb=1

valid_name="name2"
valid_protein=2
valid_fat=2
valid_carb=2

url = '/nutri/fooditem/'
factory = APIRequestFactory()
view = controller.FoodItemController.as_view()
initial_json = json.dumps({
    "name": initial_name,
    "protein": initial_protein,
    "fat": initial_fat,
    "carb": initial_carb
})

@given('there is a food item created by that user')
def step_impl(context):
    request = factory.post(url, initial_json, content_type='application/json')
    force_authenticate(request, user=context.user)
    context.fooditem_id = view(request).data['fooditem']['id']

@given('there is a food item that is not created by that user')
def step_impl(context):
    context.anotherUser = User.objects.create_user(username="testB", email="testB@email.com")

    request = factory.post(url, initial_json, content_type='application/json')
    force_authenticate(request, user=context.anotherUser)
    context.fooditem_id = view(request).data['fooditem']['id']

@when('the user requests to edit that food item’s attributes')
def step_impl(context):
    token, created = Token.objects.get_or_create(user=context.user)

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.put(
        url,
        json.dumps(context.json_request),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token ' + token.key
    )
    context.response = view(request)

@when('the user enters valid attributes')
def step_impl(context):
    context.json_request = {
        "fooditem": context.fooditem_id,
        "name": valid_name,
        "protein": valid_protein,
        "fat": valid_fat,
        "carb": valid_carb
    }

@then('the system remembers the updated food attributes')
def step_impl(context):
    fooditem = context.response.data['fooditem']
    fooditem_obj = FoodItem.objects.get(pk=context.fooditem_id)

    assert fooditem["name"] == valid_name
    assert fooditem["fat" ]== valid_fat
    assert fooditem["carb"] == valid_carb
    assert fooditem["protein"] == valid_protein

    assert fooditem_obj.name == valid_name
    assert fooditem_obj.fat == valid_fat
    assert fooditem_obj.carb == valid_carb
    assert fooditem_obj.protein == valid_protein

@then('the system does not allow the user to edit the attributes')
def step_impl(context):
    fooditem_obj = FoodItem.objects.get(pk=context.fooditem_id)
    assert fooditem_obj.name == initial_name
    assert fooditem_obj.fat == initial_fat
    assert fooditem_obj.carb == initial_carb
    assert fooditem_obj.protein == initial_protein
