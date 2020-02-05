from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from nutrition.models import FoodItem, Meal
from nutrition.serializers import FoodItemSerializer

class Test(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)

class FoodItemController(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # Gather input parameters and check for errors
        name = request.data.get('name', None)
        if name is None:
            return Response({"message": "Error: no name provided"}, status=status.HTTP_400_BAD_REQUEST) 

        protein = request.data.get('protein', None)
        if protein is None:
            return Response({"message": "Error: no protein value provided"}, status=status.HTTP_400_BAD_REQUEST) 
        if protein < 0:
            return Response({"message": "Error: negative protein provided"}, status=status.HTTP_400_BAD_REQUEST) 

        fat = request.data.get('fat', None)
        if fat is None:
            return Response({"message": "Error: no fat value provided"}, status=status.HTTP_400_BAD_REQUEST) 
        if fat < 0:
            return Response({"message": "Error: negative fat provided"}, status=status.HTTP_400_BAD_REQUEST) 

        carb = request.data.get('carb', None)
        if carb is None:
            return Response({"message": "Error: no carb value provided"}, status=status.HTTP_400_BAD_REQUEST) 
        if carb < 0:
            return Response({"message": "Error: negative carb provided"}, status=status.HTTP_400_BAD_REQUEST) 

        # Create FoodItem in database
        fooditem = FoodItem.objects.create(name=name, protein=protein, fat=fat, carb=carb)

        # Create and send response
        fooditem_serializer = FoodItemSerializer(fooditem)
        response = {
            "fooditem": fooditem_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class MealController(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        fooditem_ids = request.data.get('fooditems', [])
        name = request.data.get('name', None)

        if len(fooditem_ids) == 0:
            protein = request.data.get('protein', 0)
            fat = request.data.get('fat', 0)
            carb = request.data.get('carb', 0)

            meal = Meal.objects.create(name=name, protein=protein, carb=carb, fat=fat)
            return Response({"message": "success"}, status=status.HTTP_200_OK)

        fooditems = []
        protein = 0
        carb = 0
        fat = 0

        meal = Meal.objects.create(name=name)

        for fooditem_id in fooditem_ids:
            fooditem = FoodItem.objects.get(pk=fooditem_id)
            protein += fooditem.protein
            carb += fooditem.carb
            fat += fooditem.fat
            meal.fooditems.add(fooditem)

        meal.protein = protein
        meal.carb = carb
        meal.fat = fat

        meal.save()

        response = {
            "message": "success"
        }
        return Response(response, status=status.HTTP_200_OK)