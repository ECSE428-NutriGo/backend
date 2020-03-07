#may not be needed, will clean up later
from behave import use_fixture
#from my_django.behave_fixtures import django_test_runner, django_test_case
#import os
import django
django.setup()

from django.contrib.auth.models import User
from nutrition.models import Meal, MealEntry, FoodItem



#os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

def before_all(context):
    context.config.setup_logging()
    User.objects.all().delete()
    FoodItem.objects.all().delete()
    Meal.objects.all().delete()
    #use_fixture(django_test_runner, context)



def after_scenario(context, scenario):
    User.objects.all().delete()
    FoodItem.objects.all().delete()
    Meal.objects.all().delete()
#    use_fixture(django_test_case, context)
