from behave import *
@given('we have behave installed')
def step_impl(context):                 #write the steps to perform the given statement
    pass

@when('we implement a test')
def step_impl(context):                 #write the steps to perform the when statement
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):                 #write the steps to perform the then statement
    assert context.failed is False


# if there is a list -->
@given('a set of specific users')
def step_impl(context):
    for row in context.table:
        model.add_user(name=row['name'], department=row['department'])

# to define similar steps at the same time
@then('the result page will include "{text}"')
def step_impl(context, text):
    if text not in context.response:
        fail('%r not in %r' % (text, context.response))
