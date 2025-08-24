from rest_framework import serializers
from .models import Tag, Hero, Nomination
from authentication.serializers import UserSerializer
from rest_framework.validators import ValidationError

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description']


# I think I'll need a serializer
# to create Nomination
# One to update Nomication
# Nomination details

class NominationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomination
        fields = [
            'id',
            'slug',
            'nominee_name',
            'nominator_name',
            'status',
            'created_at',
        ]

class NominationDetailsSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)

    class Meta:
        model = Nomination
        fields = "__all__"

class NominationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nomination
        fields = [
            'nominee_name',
            'nominee_email',
            'nominee_phone',
            'nominee_location',
            'nominator_name',
            'nominator_email',
            'nominator_phone',
            'story',
            'additional_info',

            'nominated_by',
        ]
        
    def validate(self, attrs):
        if not attrs.get('nominee_email', None) and not attrs.get('nominee_phone', None):
            raise ValidationError("Nomination needs either phone or email")

        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            validated_data['nominated_by'] = request.user

            validated_data.pop('nominator_name', None)
            validated_data.pop('nominator_email', None)
            validated_data.pop('nominator_phone', None)

        return super().create(validated_data)
