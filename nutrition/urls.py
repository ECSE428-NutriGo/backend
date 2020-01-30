from django.urls import include, path
from . import controller

app_name = 'nutrition'

urlpatterns = [
    path('test/', controller.Test.as_view()),
]