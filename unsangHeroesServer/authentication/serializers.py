from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'bio',
            'role',
            'location',
            'phone_number',
            'avatar',
            'date_of_birth',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile',
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'profile'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        if profile_data:
            for key, value in profile_data.items():
                setattr(User.profile, key, value)
            user.profile.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
