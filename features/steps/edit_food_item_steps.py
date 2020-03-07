from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem

import pdb


@when('the user requests to edit a food item’s attributes')
def step_impl(context):
    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.put(
        url,
        json.dumps({
            "fooditem_id": context.FoodItem.id,
            "name": "name2",
            "protein": context.protein2,
            "fat": context.fat2,
            "carb": context.carb2}),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)
    breakpoint()
    
@when('the food item was created by that user')
def step_impl(context):
    context.FoodItem = FoodItem.objects.create(name="created by user", protein=1, fat=1, carb=1, user=context.user)
@when('the user enters valid attributes')
def step_impl(context):
    context.fooditem_name="name2"
    context.protein2=2
    context.fat2=2
    context.carb2=2

@when('the food item was not created by that user')
def step_impl(context):
    anotherUser = User.objects.create_user(username="testB", email="testB@email.com")
    context.FoodItem = FoodItem.objects.create(name="created by another user", protein=1, fat=1, carb=1, user=anotherUser)
@then('the system remembers the updated food attributes')
def step_impl(context):
    # assert context.response.status_code == 200
    breakpoint()
    fooditem = context.response.data['fooditem']
    assert fooditem.name == "name2"
    assert fooditem.fat==2
    assert fooditem.carb==2
    assert fooditem.protein==2

@then('the system does not allow the user to edit the attributes')
def step_impl(context):

    fooditem = context.response.data['fooditem']
    assert(fooditem.name== "name1")
    assert(fooditem.fat== 1)
    assert(fooditem.carb== 1)
    assert(fooditem.protein== 1)
