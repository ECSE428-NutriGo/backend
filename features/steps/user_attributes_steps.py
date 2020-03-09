from behave import *
import parse

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


@when('the user enters valid "{email}", "{age}", "{hours_activity}", "{protein_target}", "{fat_target}", "{carb_target}" for all changing attributes')
def step_impl(context, email, age, hours_activity, protein_target, fat_target, carb_target):
    context.email = email
    context.age = int(age)
    context.hours_activity = int(hours_activity)
    context.protein_target = int(protein_target)
    context.fat_target = int(fat_target)
    context.carb_target = int(carb_target)

    context.json_request = {
        "age": context.age,
        "hours_activity": context.hours_activity,
        "protein_target": context.protein_target,
        "fat_target": context.fat_target,
        "carb_target": context.carb_target 
    }

@when('the user enters some valid "{email}", "{age}", "{hours_activity}", "{protein_target}", "{fat_target}", "{carb_target}" for changing attributes and leaves other attributes blank')
def step_impl(context, email, age, hours_activity, protein_target, fat_target, carb_target):
    try:
        context.age = int(age)
    except ValueError:
        context.age = None
    try:
        context.hours_activity = int(hours_activity)
    except ValueError:
        context.hours_activity = None
    try:
        context.protein_target = int(protein_target)
    except ValueError:
        context.protein_target = None
    try:
        context.fat_target = int(fat_target)
    except ValueError:
        context.fat_target = None
    try:
        context.carb_target = int(carb_target)
    except ValueError:
        context.carb_target = None

    context.json_request = {}
    if context.age is not None:
        context.json_request["age"] = context.age
    if context.hours_activity is not None:
        context.json_request["hours_activity"] = context.hours_activity
    if context.protein_target is not None:
        context.json_request["protein_target"] = context.protein_target
    if context.fat_target is not None:
        context.json_request["fat_target"] = context.fat_target
    if context.carb_target is not None:
        context.json_request["carb_target"] = context.carb_target

@when('the user enters invalid "{email}", "{age}", "{hours_activity}", "{protein_target}", "{fat_target}", "{carb_target}" for a given attributes')
def step_impl(context, email, age, hours_activity, protein_target, fat_target, carb_target):
    context.email = email
    context.age = int(age)
    context.hours_activity = int(hours_activity)
    context.protein_target = int(protein_target)
    context.fat_target = int(fat_target)
    context.carb_target = int(carb_target)

    context.json_request = {
        "age": context.age,
        "hours_activity": context.hours_activity,
        "protein_target": context.protein_target,
        "fat_target": context.fat_target,
        "carb_target": context.carb_target 
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
    if context.age:
        assert context.response.data['age'] == context.age

    if context.hours_activity:
        assert context.response.data['hours_activity'] == context.hours_activity

    if context.protein_target:
        assert context.response.data['protein_target'] == context.protein_target

    if context.fat_target:
        assert context.response.data['fat_target'] == context.fat_target

    if context.carb_target:
        assert context.response.data['carb_target'] == context.carb_target

@then('the system will not register the new user attributes for the invalid data')
def step_impl(context):
    if context.age < 0:
        assert context.response.data['age'] != context.age
    else:
        assert context.response.data['age'] == context.age

    if context.hours_activity < 0:
        assert context.response.data['hours_activity'] != context.hours_activity
    else:
        assert context.response.data['hours_activity'] == context.hours_activity

    if context.protein_target < 0:
        assert context.response.data['protein_target'] != context.protein_target
    else:
        assert context.response.data['protein_target'] == context.protein_target

    if context.fat_target < 0:
        assert context.response.data['fat_target'] != context.fat_target
    else:
        assert context.response.data['fat_target'] == context.fat_target

    if context.carb_target < 0:
        assert context.response.data['carb_target'] != context.carb_target
    else:
        assert context.response.data['carb_target'] == context.carb_target

