from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from profile.serializers import UserSerializer

from django.contrib.auth.models import User
from profile.models import Profile

class LockOutUser(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    #
    # Lock out a given user
    #
    def post(self, request):
        user_email = request.data.get('email', None)

        if user_email is None:
            return Response({"message": "Error: Please provide a user email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=user_email)
        except ObjectDoesNotExist:
            return Response({"message": "Error: Provided email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = False
        user.save()

        response = {
            "message": "User " + user_email + " is locked out"
        }
        
        return Response(response, status=status.HTTP_200_OK)

    #
    # Unlock a given user
    #
    def put(self, request):
        user_email = request.data.get('email', None)

        if user_email is None:
            return Response({"message": "Error: Please provide a user email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=user_email)
        except ObjectDoesNotExist:
            return Response({"message": "Error: Provided email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        response = {
            "message": "User " + user_email + " is unlocked"
        }
        
        return Response(response, status=status.HTTP_200_OK)


class UserSearch(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        keyword = request.query_params.get('keyword', None)

        if keyword is None:
            users = User.objects.all()
        else:
            users = User.objects.filter(username__icontains=keyword)
            if users.__len__() < 1:
                return Response({"message": "Error: no names contain " + keyword}, status=status.HTTP_400_BAD_REQUEST)


        users_serializers = []

        for user in users:
            users_serializers.append(UserSerializer(user).data)

        response = {
            "users": users_serializers
        }

        return Response(response, status=status.HTTP_200_OK)

class IndividualUserSearch(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user_email = request.query_params.get('email', None)

        if user_email is None:
            return Response({"message": "Error: Please provide a user email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=user_email)
        except ObjectDoesNotExist:
            return Response({"message": "Error: Provided email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(user).data

        response = {
            "user": user_serializer
        }

        return Response(response, status=status.HTTP_200_OK)