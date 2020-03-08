from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework.utils import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@when('the user requests to edit the attributes of their profile')
def step_impl(context):
    token, created = Token.objects.get_or_create(user=context.user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    context.response = client.put('/rest-auth/user/', context.json_request, format='json')


@when('the user enters valid information for all changing attributes')
def step_impl(context):
    context.email = "validEmail@email.com"
    context.age = 25
    context.hours_activity = 20
    context.protein_target = 100
    context.fat_target = 101
    context.carb_target = 102

    context.json_request = {
        "age": context.age,
        "hours_activity": context.hours_activity,
        "protein_target": context.protein_target,
        "fat_target": context.fat_target,
        "carb_target": context.carb_target 
    }

@when('the user enters some valid information for changing attributes and leaves other attributes blank')
def step_impl(context):
    context.hours_activity = 20
    context.carb_target = 102

    context.json_request = {
        "hours_activity": context.hours_activity,
        "carb_target": context.carb_target 
    }

@when('the user enters invalid information for a given attributes')
def step_impl(context):
    context.age = -1

    context.json_request = {
        "age": context.age,
    }

@then('the system will register the new user attributes for the user')
def step_impl(context):
    assert context.response.data['age'] == context.age
    assert context.response.data['hours_activity'] == context.hours_activity
    assert context.response.data['protein_target'] == context.protein_target
    assert context.response.data['fat_target'] == context.fat_target
    assert context.response.data['carb_target'] == context.carb_target

@then('the system will register the new user attributes for the ones changed and will keep the old attributes for the fields left blank')
def step_impl(context):
    assert context.response.data['hours_activity'] == context.hours_activity
    assert context.response.data['carb_target'] == context.carb_target

@then('the system will not register the new user attributes for the invalid data')
def step_impl(context):
    assert context.response.data['age'] != context.age
