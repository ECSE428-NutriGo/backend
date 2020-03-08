from behave import *



from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User

factory = APIRequestFactory()

@given('NutriGo {text} is logged into the application')
def step_impl(context, text):                 #write the steps to perform the given statement
    email = "testA@email.com"
    # username = "testA"
    user = User.objects.create_user(username=email, email=email)
    if text == "user":
        context.user = user
    elif text == "admin":
        user.is_staff = True
        user.is_admin = True
        user.save()
        context.user = user
    else:
        fail('not a valid user type of the system')

@given('another user exists in the system')
def step_impl(context):
    email = "testB@email.com"
    user = User.objects.create_user(username=email, email=email)
    context.user2 = user




@then('a "{text}" message is issued')
def step_impl(context, text):
    assert context.message == text

@then('the {text} should see a confirmation message')
def step_impl(context, text):
    assert context.response.status_code >= 200
    assert context.response.status_code < 300

@then('the {text} should see an error message')
def step_impl(context, text):
    assert context.response.status_code >= 400
    assert context.response.status_code < 600
