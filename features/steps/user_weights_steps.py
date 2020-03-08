from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework.utils import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profile import controller

@when('the user enters valid information for their {text} weight')
def step_impl(context, text):
    context.input_weight = 100

@when('the user enters invalid number for their {text} weight')
def step_impl(context, text):
    context.input_weight = -1

@when('the user requests to edit the {text} weight of their profile')
def step_impl(context, text):
    if text == "current":
        pass    #TODO get type specifics
    elif text == "target":
        pass    #TODO get type specifics
    else:
        fail('this test is not yet implemented for: ' + text + 'weight ')

    token, created = Token.objects.get_or_create(user=context.user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    context.response = client.put('/rest-auth/user/', {
        text+"_weight": context.input_weight
    }, format='json')

@then('the system will register the new {text} weight for the user')
def step_impl(context, text):

    assert context.input_weight == context.response.data[text+"_weight"]

@then('the system will maintain the old {text} weight for the user’s profile')
def step_impl(context, text):

    assert context.input_weight != context.user.profile.current_weight
