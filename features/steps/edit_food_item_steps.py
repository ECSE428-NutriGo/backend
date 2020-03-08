from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
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
    context.name1 = "name1"
    context.protein1 = 1
    context.fat1 = 1
    context.carb1 = 1

    context.name2 = "name2"
    context.protein2 = 2
    context.fat2 = 2
    context.carb2 = 2

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()

    request = factory.post(
        url,
        json.dumps({
            "name": context.name1,
            "protein": context.protein1,
            "fat": context.fat1,
            "carb": context.carb1
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.fooditem_id = view(request).data['fooditem']['id']

@given('there is a food item that is not created by that user')
def step_impl(context):
    context.anotherUser = User.objects.create_user(username="testB", email="testB@email.com")

    context.name1 = "name1"
    context.protein1 = 1
    context.fat1 = 1
    context.carb1 = 1

    context.name2 = "name2"
    context.protein2 = 2
    context.fat2 = 2
    context.carb2 = 2

    url = '/nutri/fooditem/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()

    request = factory.post(
        url,
        json.dumps({
            "name": context.name1,
            "protein": context.protein1,
            "fat": context.fat1,
            "carb": context.carb1
        }),
        content_type='application/json'
    )
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
        "name": context.name2,
        "protein": context.protein2,
        "fat": context.fat2,
        "carb": context.carb2
    }

@then('the system remembers the updated food attributes')
def step_impl(context):
    print(context.response.data)
    fooditem = context.response.data['fooditem']
    fooditem_obj = FoodItem.objects.get(pk=context.fooditem_id)

    assert fooditem["name"] == context.name2
    assert fooditem["fat" ]== context.fat2
    assert fooditem["carb"] == context.carb2
    assert fooditem["protein"] == context.protein2

    assert fooditem_obj.name == context.name2
    assert fooditem_obj.fat == context.fat2
    assert fooditem_obj.carb == context.carb2
    assert fooditem_obj.protein == context.protein2

@then('the system does not allow the user to edit the attributes')
def step_impl(context):
    fooditem_obj = FoodItem.objects.get(pk=context.fooditem_id)
    print(fooditem_obj)
    assert fooditem_obj.name == context.name1
    assert fooditem_obj.fat == context.fat1
    assert fooditem_obj.carb == context.carb1
    assert fooditem_obj.protein == context.protein1
    
