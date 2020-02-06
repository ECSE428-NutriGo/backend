from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.
class FoodItem(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='fooditems', on_delete=models.SET_NULL)
    name = models.CharField(default='', max_length=512)
    protein = models.IntegerField(default=0)
    carb = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Meal(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='meals', on_delete=models.SET_NULL)
    fooditems = models.ManyToManyField(FoodItem, related_name='meals')
    name = models.CharField(default='', max_length=512)
    protein = models.IntegerField(default=0)
    carb = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class MealEntry(models.Model):
    user = models.ForeignKey(User, related_name='mealentries', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, related_name='mealentries', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.meal.name + " - " + str(self.timestamp)
