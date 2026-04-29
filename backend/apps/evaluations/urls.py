from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluationViewSet, StudentProgressViewSet

router = DefaultRouter()
router.register('', EvaluationViewSet, basename='evaluation')
router.register('progress', StudentProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
]
