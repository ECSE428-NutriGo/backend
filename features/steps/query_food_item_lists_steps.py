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

url = '/nutri/fooditem/'
factory = APIRequestFactory()
view = controller.FoodItemController.as_view()

@given('food items have been created')
def step_impl(context):
    fi1 = factory.post(
        url,
        json.dumps({
            'name': name1,
            'fat': fat1,
            'protein': protein1,
            'carb': carb1
        }),
        content_type='application/json'
    )
    fi2 = factory.post(
        url,
        json.dumps({
            'name': name2,
            'fat': fat2,
            'protein': protein2,
            'carb': carb2
        }),
        content_type='application/json'
    )
    fi3 = factory.post(
        url,
        json.dumps({
            'name': name3,
            'fat': fat3,
            'protein': protein3,
            'carb': carb3
        }),
        content_type='application/json'
    )
    force_authenticate(fi1, context.user)
    force_authenticate(fi2, context.user)
    force_authenticate(fi3, context.user)
    view(fi1)
    view(fi2)
    view(fi3)

@when('the user enters a valid search filter to filter the results')
def step_impl(context):
    context.filter = "m 1"

@when('the user requests to query food items in the system')
def step_impl(context):
    if not hasattr(context, 'filter') or context.filter is None:
        request = factory.get(url)
    else:
        request = factory.get(
            url,
            {'filter': context.filter},
            format='application/json'
        )

    force_authenticate(request, context.user)
    context.response = view(request)

@when('no food items in the system contain the search filter')
def step_impl(context):
    context.filter = "not a fooditem"

@then('the system displays a list of all food items')
def step_impl(context):
    context.response.data['fooditems']==3

@then('the system displays a list of food items containing the search filters')
def step_impl(context):
    context.response.data['fooditems']==1

@then('the user then enters a valid search filter to filter the results')
def step_impl(context):
    pass
@then('the system filters the current results to only those containing the search filters')
def step_impl(context):
    pass
