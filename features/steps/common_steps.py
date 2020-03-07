from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from nutrition import controller
from nutrition.models import Meal, MealEntry, FoodItem

@given('NutriGo {text} is logged into the application')
def step_impl(context, text):                 #write the steps to perform the given statement
    email = "testA@email.com"
    username = "testA"

    if text == "user"
        context.user = User.objects.create_user(username=username, email=email)
    else if text == "admin"
        context.user = User.objects.create_user(username=username, email=email) #TODO admin version
    else fail('not a valid user type of the system')


@then('a "{text}" message is issued')
def step_impl(context, text):
    assert context.message == text
