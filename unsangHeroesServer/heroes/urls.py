from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, NominationViewSet, InterviewViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tag')
router.register(r'nominations', NominationViewSet, basename='nomination')
router.register(r'interviews', InterviewViewSet, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
]
