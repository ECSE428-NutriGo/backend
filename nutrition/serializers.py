from rest_framework import serializers

from nutrition.models import FoodItem, Meal, MealEntry

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'