from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem

import pdb

@given('there is a food item created by that user')
def step_impl(context):
    name1 = "name1"
    protein1 = 1
    fat1 = 1
    carb1 = 1

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()

    request = factory.post(
        url,
        json.dumps({
            "name": name1,
            "protein": protein1,
            "fat": fat1,
            "carb": carb1
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.fooditem_id = view(request).data['fooditem']['id']

@given('there is a food item that is not created by that user')
def step_impl(context):
    anotherUser = User.objects.create_user(username="testB", email="testB@email.com")

    name1 = "name1"
    protein1 = 1
    fat1 = 1
    carb1 = 1

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()

    request = factory.post(
        url,
        json.dumps({
            "name": name1,
            "protein": protein1,
            "fat": fat1,
            "carb": carb1
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=anotherUser)
    context.fooditem_id = view(request).data['fooditem']['id']


@when('the user requests to edit that food item’s attributes')
def step_impl(context):
    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.get(url)
    force_authenticate(request, user=context.user)
    response = view(request)
    fooditem = response.data['fooditems'][0]

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.put(
        url,
        json.dumps({
            "fooditem": context.fooditem_id,
            "name": "name2",
            "protein": 2,
            "fat": 2,
            "carb": 2
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)

@when('the user enters valid attributes')
def step_impl(context):
    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.get(url)
    force_authenticate(request, user=context.user)
    response = view(request)

    context.fooditem_name="name2"
    context.protein2=2
    context.fat2=2
    context.carb2=2

@then('the system remembers the updated food attributes')
def step_impl(context):
    fooditem = context.response.data['fooditem']
    assert fooditem["name"] == "name2"
    assert fooditem["fat"]==2
    assert fooditem["carb"]==2
    assert fooditem["protein"]==2

@then('the system does not allow the user to edit the attributes')
def step_impl(context):

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.get(url)
    force_authenticate(request, user=context.user)
    response = view(request)
    fooditem = response.data['fooditems'][0]

    assert fooditem["name"] == "name1"
    assert fooditem["fat"] == 1
    assert fooditem["carb"] == 1
    assert fooditem["protein"] == 1

@then('the response should be a success')
def step_impl(context):
    assert context.response.status_code == 200

@then('the user should see an error message')
def step_impl(context):
    assert context.response.status_code >= 300
