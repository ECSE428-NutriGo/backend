from django.contrib import admin
from nutrition.models import FoodItem, Meal, MealEntry

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(Meal)
admin.site.register(MealEntry)
