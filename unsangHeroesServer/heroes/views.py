from rest_framework.viewsets import ModelViewSet
from .serializers import (
    TagSerializer,
    NominationListSerializer,
    NominationDetailSerializer,
    NominationCreateSerializer,
    InterviewCreateSerializer,
    InterviewDetailSerializer,
    InterviewListSerializer,
    StoryCreateSerializer,
    StoryDetailSerializer,
    StoryListSerializer,
)
from .permissions import CanWriteOrReadOnly
from .models import (
    Tag,
    Hero,
    Nomination,
    Interview,
    Story,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

class NominationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user
        if user.profile.role != 'public':
            return Nomination.objects.all()
        return Nomination.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return NominationListSerializer

        if self.action == 'create':
            return NominationCreateSerializer

        if self.action == 'retreive':
            return NominationDetailSerializer

        return NominationDetailSerializer

class InterviewViewSet(ModelViewSet):
    queryset = Interview.objects.all()
    permission_classes = [CanWriteOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return InterviewListSerializer

        if self.action == 'create':
            return InterviewCreateSerializer

        if self.action == 'retreive':
            return InterviewDetailSerializer

        return InterviewDetailSerializer

class StoryViewSet(ModelViewSet):
    queryset = Story.objects.all()
    permission_classes = [CanWriteOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return StoryListSerializer

        if self.action in ['create', 'update', 'partial_update']:
            return StoryCreateSerializer

        if self.action == 'retreive':
            return StoryDetailSerializer

        return StoryDetailSerializer
