from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller


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
    creation_request = factory.post(url, initial_json, content_type='application/json')
    force_authenticate(creation_request, user=context.user)
    response = view(creation_request)
    context.fooditem_id = response.data['fooditem']['id']

@given('there is a food item that is not created by that user')
def step_impl(context):
    creation_request = factory.post(url, initial_json, content_type='application/json')
    anotherUser = User.objects.create_user(username="testB", email="testB@email.com")
    force_authenticate(creation_request, user=anotherUser)
    response = view(creation_request)
    context.fooditem_id = response.data['fooditem']['id']


@when('the user requests to edit that food item’s attributes')
def step_impl(context):
    request = factory.put(
        url,
        json.dumps({
            "fooditem": context.fooditem_id,
            "name": context.fooditem_name,
            "protein": context.protein2,
            "fat": context.fat2,
            "carb": context.carb2
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)

@when('the user enters valid attributes')
def step_impl(context):
    context.fooditem_name=valid_name
    context.protein2=valid_protein
    context.fat2=valid_fat
    context.carb2=valid_carb

@then('the system remembers the updated food attributes')
def step_impl(context):
    fooditem = context.response.data['fooditem']
    assert fooditem["name"] == valid_name
    assert fooditem["fat"]==valid_fat
    assert fooditem["carb"]==valid_carb
    assert fooditem["protein"]==valid_protein

@then('the system does not allow the user to edit the attributes')
def step_impl(context):
    request = factory.get(url)
    force_authenticate(request, user=context.user)
    response = view(request)
    fooditem = response.data['fooditems'][0]

    assert fooditem["name"] == initial_name
    assert fooditem["fat"] == initial_fat
    assert fooditem["carb"] == initial_carb
    assert fooditem["protein"] == initial_carb
