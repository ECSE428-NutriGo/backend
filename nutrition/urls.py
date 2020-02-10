from django.urls import include, path
from . import controller

app_name = 'nutrition'

urlpatterns = [
    path('fooditem/', controller.FoodItemController.as_view()),
    path('meal/', controller.MealController.as_view()),
    path('mealentry/', controller.MealEntryController.as_view())
    
]