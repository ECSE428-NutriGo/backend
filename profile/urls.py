from django.urls import include, path
from . import controller

app_name = 'profile'

urlpatterns = [
    path('lockout/', controller.LockOutUser.as_view()),
]