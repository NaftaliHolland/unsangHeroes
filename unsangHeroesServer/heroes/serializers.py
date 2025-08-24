from rest_framework import serializers
from .models import Tag, Hero, Nomination, Interview
from authentication.serializers import UserSerializer
from rest_framework.validators import ValidationError

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description']

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

class NominationDetailSerializer(serializers.ModelSerializer):

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

class InterviewListSerializer(serializers.ModelSerializer):
    nomination_name = serializers.CharField(source='nomination.nominee_name', read_only=True)
    interviewer_name = serializers.CharField(source='interviewer.username', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id',
            'nomination_name',
            'interviewer_name',
            'scheduled_at',
            'status',
        ]

class InterviewDetailSerializer(serializers.ModelSerializer):
    nomination = serializers.StringRelatedField()
    interviewer = serializers.StringRelatedField()

    class Meta:
        model = Interview
        fields = [
            'id',
            'nomination',
            'interviewer',
            'scheduled_at',
            'location',
            'notes',
            'status',
            'created_at',
            'updated_at',
        ]

class InterviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            'nomination',
            'interviewer',
            'scheduled_at',
            'location',
            'notes',
            'status',
        ]

    def validate(self, attrs):
        if not attrs.get('nomination', None):
            raise ValidationError("Interview has to have a nomination")
        if not attrs.get('interviewer', None):
            raise ValidationError("Interview has to have an interviewer")
        if attrs.get('sheduled_at', None):
            from django.utils import timezone
            if attrs['sheduled_at'] < timezone.now():
                raise serializers.ValidationError("Interview date must be in the future.")

        return super().validate(attrs)
