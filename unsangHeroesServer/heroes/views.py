from rest_framework.viewsets import ModelViewSet
from .serializers import (
    TagSerializer,
    NominationListSerializer,
    NominationDetailsSerializer,
    NominationCreateSerializer,
)
from .models import Tag, Hero, Nomination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

class NominationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user
        if user.profile.role is not 'public':
            return Nomination.objects.all()
        return Nomination.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return NominationListSerializer

        if self.action == 'create':
            return NominationCreateSerializer

        if self.action == 'retreive':
            return NominationDetailsSerializer

        return NominationDetailsSerializer
