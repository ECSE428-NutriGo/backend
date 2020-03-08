from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile.serializers import UserSerializer
from profile import controller

import pdb

url = '/profile/user/'
factory = APIRequestFactory()
view = controller.IndividualUserSearch.as_view()

invalid_email = "not an email"

@when('the System Admin enters the appropriate filter to search the individual user of the system')
def step_impl(context):
    context.filter = context.user2.email
@when('the System Admin enters an incorrect filter to search the individual user of the system')
def step_impl(context):
    context.filter = invalid_email
@when('the System Admin requests to view the attributes of an individual user of the system')
def step_impl(context):
    data = {"email": context.filter}
    request = factory.get(
        url,
        data,
        format='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)

@then('the system will fetch the attributes of the requested user')
def step_impl(context):
    serializedData = UserSerializer(context.user2).data
    assert serializedData == context.response.data['user']

@then('the System Admin should see the attributes of the user')
def step_impl(context):
    pass

@then('the system will not fetch the attributes of the requested user')
def step_impl(context):
    assert 'user' not in context.response.data.keys()
