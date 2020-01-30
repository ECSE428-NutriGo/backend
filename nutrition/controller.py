from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class Test(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        
        return Response({"messge": "Hello, world!"}, status=status.HTTP_200_OK)
