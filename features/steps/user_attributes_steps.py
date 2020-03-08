from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile import controller

valid_email = "validEmail@email.com"
valid_age = 25
valid_hours_activity = 20

invalid_age = -1

url = '/profile/'
factory = APIRequestFactory()
view = controller.FoodItemController.as_view()

@when('the user requests to edit the attributes of their profile')
def step_impl(context):
    # TODO: get the old data to compare against, store in oldData

    context.oldEmail = oldData.email
    context.oldAge = oldData.age
    context.oldHours_activity = oldData.hours_activity

    request = factory.put(
        url,
        json.dumps({
            "email": context.email,
            "hours_activity": context.hours_activity,
            "age": context.age
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)


@when('the user enters valid information for all changing attributes')
def step_impl(context):
    context.email = valid_email
    context.age = valid_age
    context.hours_activity = valid_hours_activity

@when('the user enters some valid information for changing attributes and leaves other attributes blank')
def step_impl(context):
    context.email = None
    context.age = valid_age
    context.hours_activity = valid_hours_activity

@when('the user enters invalid information for a given attributes')
def step_impl(context):
    context.email = valid_email
    context.age = invalid_age
    context.hours_activity = valid_hours_activity

@then('the system will register the new user attributes for the user')
def step_impl(context):
    #TODO get from database
    assert response.email == context.email
    assert response.age == context.age
    assert response.hours_activity == context.hours_activity

@then('the system will register the new user attributes for the ones changed and will keep the old attributes for the fields left blank')
def step_impl(context):
    if context.email is None:
        assert response.email == context.oldEmail
    else:
        assert response.email == context.email
    if context.age is None:
        assert response.age == context.oldAge
    else:
        assert response.age == context.age
    if context.hours_activity is None:
        assert response.hours_activity == context.oldHours_activity
    else:
        assert response.hours_activity == context.hours_activity

@then('the system will not register the new user attributes for the invalid data')
def step_impl(context):
    assert response.email == context.oldEmail
    assert response.age == context.oldAge
    assert response.hours_activity == context.oldHours_activity
