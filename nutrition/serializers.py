from rest_framework import serializers

from nutrition.models import FoodItem, Meal, MealEntry

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class MealEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealEntry
        fields = '__all__'