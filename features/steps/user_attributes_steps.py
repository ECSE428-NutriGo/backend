from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User

@when('the user requests to edit the attributes of their profile')
def step_impl(context):
    url = '/rest-auth/user/'
    factory = APIRequestFactory()
    view = controller.FoodItemController.as_view()
    request = factory.put(
        url,
        json.dumps({
            "email": context.email,
            "protein_target": context.protein_target,       #TODO other attributes
            "age": context.age
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)


@when('the user enters valid information for all changing attributes')
def step_impl(context):
    context.email = "validEmail@email.com"
    context.age = 25
    #TODO any other attributes


@when('the user enters some valid information for changing attributes and leaves other attributes blank')
def step_impl(context):
    context.email = None
    context.age = 30
    #TODO any other attributes


@when('the user enters invalid information for a given attributes')
def step_impl(context):
    context.email = "validEmail@email.com"
    context.age = -1
    #TODO any other attributes

@then('the system will register the new user attributes for the user')
def step_impl(context):
    #TODO get from database
    assert response.email == context.email
    assert response.age == context.age
    # TODO:  any remaining attributes

@then('the system will register the new user attributes for the ones changed and will keep the old attributes for the fields left blank')
def step_impl(context):
    assert response.email == context.oldEmail
    assert response.age == context.age
    # TODO:  any remaining attributes

@then('the system will not register the new user attributes for the invalid data')
def step_impl(context):
    assert response.email == context.oldEmail
    assert response.age == context.oldAge
    # TODO:  any remaining attributes
