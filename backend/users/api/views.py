from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    Register new account
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
