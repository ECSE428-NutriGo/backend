from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile import controller

valid_weight = 100
invalid_weight = -1

url = '/profile/'
factory = APIRequestFactory()
view = controller.FoodItemController.as_view()      #TODO get necessary view

@when('the user enters valid information for their {text} weight')
def step_impl(context, text):
    context.input_weight = valid_weight

@when('the user enters invalid number for their {text} weight')
def step_impl(context, text):
    context.input_weight = invalid_weight

@when('the user requests to edit the {text} weight of their profile')
def step_impl(context, text):
    if text == "current":
        url = '/nutri/fooditem/'        #TODO get url
    elif text == "target":
        url = '/nutri/fooditem/'        #TODO get url
    else:
        fail('this test is not yet implemented for: ' + text + 'weight ')

    input_json = json.dumps({
        text+"_weight": context.input_weight
    })
    request = factory.put(url,input_json,content_type='application/json')
    force_authenticate(request, user=context.user)
    context.response = view(request)

@then('the system will register the new {text} weight for the user')
def step_impl(context, text):
    url = '/nutri/fooditem/'        #TODO get url

    request = factory.get(url)
    force_authenticate(request, user=context.user)
    response = view(request)

    # assert input_weight == response.data[]          #TODO verify new input

@then('the system will maintain the old {text} weight for the user’s profile')
def step_impl(context, text):
    url = '/nutri/fooditem/'        #TODO get url

    request = factory.get(url)
    force_authenticate(request, user=context.user)
    response = view(request)

    # assert == response.data[]          #TODO verify old input
