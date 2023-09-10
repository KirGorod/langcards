from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Wrong username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'user_id': user.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

    def get_object(self):
        return self.request.user


class GoogleAuthView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            id_info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )

            if 'email' not in id_info:
                return Response(
                    {"error": "Invalid token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"error": "Token validation failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, _ = User.objects.get_or_create(
            username=id_info['email'],
            defaults={
                'email': id_info['email'],
                'first_name': id_info.get('given_name', ''),
                'last_name': id_info.get('family_name', '')
            }
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": str(token)}, status=status.HTTP_200_OK)
