from rest_framework import serializers
from .models import Tag, Hero, Nomination, Interview, Story
from authentication.serializers import UserSerializer
from rest_framework.validators import ValidationError
from unsangheroes.utils import get_cloudinary_url

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

class StoryListSerializer(serializers.ModelSerializer):
    hero_name = serializers.CharField(source='hero.name', read_only=True)

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'hero_name',
            'intro',
            'status',
            'impact',
            'created_at'
        ]

class NestedHeroSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Hero
        fields = [
            'id',
            'display_name',
            'bio',
            'avatar',
            'location',
            'tags'
        ]

    def get_avatar(self, obj):
        variants = {
            'small': get_cloudinary_url(obj.cover_image, 50, 50),
            'medium': get_cloudinary_url(obj.cover_image, 150, 150),
            'large': get_cloudinary_url(obj.cover_image, 300, 300),
        }

        return variants

class StoryDetailSerializer(serializers.ModelSerializer):
    hero = NestedHeroSerializer(read_only=True)
    nomination_id = serializers.UUIDField(source='nomination.id', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    cover_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'hero',
            'cover_image',
            'nomination_id',
            'content',
            'intro',
            'impact',
            'history',
            'status',
            'author',
            'created_at',
            'validated_at',
            'approved_by_name',
            'approved_at'
        ]

    def get_cover_image(self, obj):

        variants = {
            'original': get_cloudinary_url(obj.cover_image),
            'desktop': get_cloudinary_url(obj.cover_image, 1200, 600),
            'tablet': get_cloudinary_url(obj.cover_image, 800, 400),
            'mobile': get_cloudinary_url(obj.cover_image, 400, 200),
        }

        return variants

class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            'hero',
            'nomination',
            'title',
            'content',
            'impact',
            'status',
            'author',
        ]
        read_only_fields = ['author']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)

    def validate(self, attrs):
        if not attrs.get('hero', None):
            raise ValidationError('hero cannot be empty')

        return super().validate(attrs)
