from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem

name1 = 'item 1'
name2 = 'item 2'
name3 = 'item 3'
protein1 = 10
protein2 = 20
protein3 = 30
fat1 = 6
fat2 = 7
fat3 = 8
carb1 = 22
carb2 = 33
carb3 = 44

url = '/nutri/meal/'
factory = APIRequestFactory()
view = controller.MealController.as_view()

@given('there are food items available')
def step_impl(context):
    context.fi1 = FoodItem.objects.create(user=context.user, protein=protein1, carb=carb1, fat=fat1, name=name1)
    context.fi2 = FoodItem.objects.create(user=context.user, protein=protein2, carb=carb2, fat=fat2, name=name2)
    context.fi3 = FoodItem.objects.create(user=context.user, protein=protein3, carb=carb3, fat=fat3, name=name3)
    context.allfis = [context.fi1.id, context.fi2.id, context.fi3.id]

@given('there is a meal that was created by the user')
def step_impl(context):
    request = factory.post(
        url,
        json.dumps({
            "fooditems": context.allfis,
            "name": 'a meal'
        }),
        content_type='application/json'
    )
    force_authenticate(request, context.user)
    context.response_initial = view(request)
    context.meal=context.response_initial.data['meal']
    if context.response_initial.status_code < 200 or context.response_initial.status_code >= 300:
        fail('unable to create meal')



@given('there is a meal that was created by another user')
def step_impl(context):
    context.anotherUser = User.objects.create_user(username="testB", email="testB@email.com")
    request = factory.post(
        url,
        json.dumps({
            "fooditems": context.allfis,
            "name": 'a meal'
        }),
        content_type='application/json'
    )
    force_authenticate(request, context.anotherUser)
    context.response_initial = view(request)
    context.meal=context.response_initial.data['meal']
    if context.response_initial.status_code < 200 or context.response_initial.status_code >= 300:
        fail('unable to create meal')

@when('the user selects a valid food item to remove')
def step_impl(context):
    context.removefi = context.fi1

@when('the user requests to remove a food item from that meal')
def step_impl(context):
    request = factory.patch(
        url,
        json.dumps({
            "fooditem": context.removefi.id,
            'meal': context.meal['id']
        }),
        content_type='application/json'
    )
    force_authenticate(request, context.user)
    context.response = view(request)

@then('the system remembers the updated meal')
def step_impl(context):
    request = factory.get(url)
    force_authenticate(request, context.user)
    response = view(request)
    assert len(response.data['meals'][0]['fooditems']) == 2

@then('the system does not allow the user to remove the given food item')
def step_impl(context):
    request = factory.get(url)
    force_authenticate(request, context.user)
    response = view(request)
    assert len(response.data['meals'][0]['fooditems']) == 3
