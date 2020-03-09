from behave import *

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.utils import json

from django.contrib.auth.models import User
from profile import controller

url = '/profile/users/'
factory = APIRequestFactory()
view = controller.UserSearch.as_view()


@when('the System Admin enters appropriate filters of search')
def step_impl(context):
    context.filter = 'B'

@when('no users within the system match the filter criteria')
def step_impl(context):
    context.filter = 'testC'

@when('the System Admin requests to view the users of the system')
def step_impl(context):

    if hasattr(context, 'filter'):
        request = factory.get(
            url,
            {'keyword': context.filter},
            format='application/json'
        )
    else:
        request = factory.get(url)
    force_authenticate(request, user=context.user)
    context.response = view(request)

@then('the System will fetch the users of the system')
def step_impl(context):
    assert len(context.response.data['users']) == 2
    assert context.response.data['users'][0]['email'] == context.user.email or context.response.data['users'][0]['email'] == context.user2.email
    assert context.response.data['users'][1]['email'] == context.user.email or context.response.data['users'][1]['email'] == context.user2.email

@then('the system will fetch the users of the system that satisfy the filters')
def step_impl(context):
    assert len(context.response.data['users']) == 1
    assert context.response.data['users'][0]['email'] == 'testB@email.com'

@then('the system will display no users')
def step_impl(context):
    if hasattr(context.response.data, 'users'):
        if len(ontext.response.data['users']) > 0:
            fail('users were displayed')
