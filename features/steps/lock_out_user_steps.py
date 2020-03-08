from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile import controller

import pdb

url = '/profile/lockout/'
factory = APIRequestFactory()
view = controller.LockOutUser.as_view()

@when('the admin requests to suspend a user')
def step_impl(context):
    request = factory.post(
        url,
        json.dumps({
            "email": context.user2.email,
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=context.user)
    context.response = view(request)

@when('the admin provides confirmation to the system')
def step_impl(context):
    pass
@then('the System will suspend the User from the system')
def step_impl(context):
    # data = {"email": context.user2.email}
    # request = factory.get(
    #     '/profile/user/',
    #     data,
    #     format='application/json'
    # )
    # force_authenticate(request, user=context.user)
    # response = controller.IndividualUserSearch.as_view()(request)
    # breakpoint()
    # assert response.data['user']['is_active'] is False
    assert context.response.data['message'] == "User " + context.user2.email + " is locked out"
