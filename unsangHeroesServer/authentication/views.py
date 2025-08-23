from django.contrib.auth.models import User
from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserSerializer
)
from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            user_serializer = UserSerializer(user)
            return Response({
                'user': user_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Registration successful'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    user_serializer = UserSerializer(user)

                    return Response({
                        'user': user_serializer.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': 'Login successful'
                    })
                else:
                    return Response({
                        'error': 'User account is disabled'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile
