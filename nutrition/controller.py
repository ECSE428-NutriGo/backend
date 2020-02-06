from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from nutrition.models import FoodItem, Meal, MealEntry
from nutrition.serializers import FoodItemSerializer, MealSerializer, MealEntrySerializer

class Test(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)

class FoodItemController(APIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    #
    # This method creates a food item given protein, carb, fat and a name
    # The created food item is returned on success with status code 200
    #
    def post(self, request):
        # Gather input parameters and check for errors
        user = request.user
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
        fooditem = FoodItem.objects.create(name=name, protein=protein, fat=fat, carb=carb, user=user)

        # Create and send response
        fooditem_serializer = FoodItemSerializer(fooditem)
        response = {
            "fooditem": fooditem_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class MealController(APIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    #
    # This method creates a meal given a list of fooditem ids and a name in the request.data
    # If a list of food items are not present, then the method checks if macronutrients values
    #      were given directly, in which case it creates a meal with no food items
    # The created meal is returned on success with status code 200
    #
    def post(self, request):
        fooditem_ids = request.data.get('fooditems', [])
        name = request.data.get('name', None)
        user = request.user

        # Check if name provided
        if name is None:
            return Response({"message": "Error: no name provided"}, status=status.HTTP_400_BAD_REQUEST)

        # use given protein, fat, and carb data if no food items
        if len(fooditem_ids) == 0:
            protein = request.data.get('protein', 0)
            fat = request.data.get('fat', 0)
            carb = request.data.get('carb', 0)

            meal = Meal.objects.create(name=name, protein=protein, carb=carb, fat=fat, user=user)
            meal_serializer = MealSerializer(meal)
            response = {
                "meal": meal_serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        # food items given, add to meal and calculate macros
        fooditems = []
        protein = 0
        carb = 0
        fat = 0
        meal = Meal.objects.create(name=name, user=user)

        # total macro nutrients and add fooditems to meal
        for fooditem_id in fooditem_ids:
            fooditem = FoodItem.objects.get(pk=fooditem_id)
            protein += fooditem.protein
            carb += fooditem.carb
            fat += fooditem.fat
            meal.fooditems.add(fooditem)

        # set total macronutrients
        meal.protein = protein
        meal.carb = carb
        meal.fat = fat

        # save meal to database
        meal.save()

        # Create and send response
        meal_serializer = MealSerializer(meal)
        response = {
            "meal": meal_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class MealEntryController(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    #
    # This method creates a meal entry given a date stamp and a Meal name in the request.data
    # The created meal entry is returned on success with status code 200
    #
    def post(self, request):

        user = request.user
 
        meal_id = request.data.get('meal', None)

        if meal_id is None:
            return Response({"message": "Error: no meal provided"}, status=status.HTTP_400_BAD_REQUEST) 

        meal = Meal.objects.get(pk=meal_id)
        mealentry = MealEntry.objects.create(user=user, meal=meal)

        mealentry_serializer = MealEntrySerializer(mealentry)
        response = {
            "mealentry": mealentry_serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)



        

