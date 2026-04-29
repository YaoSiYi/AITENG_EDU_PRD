from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatsViewSet, ExcellentStudentViewSet, InterviewQuestionViewSet

router = DefaultRouter()
router.register('', StatsViewSet, basename='stats')
router.register('excellent-students', ExcellentStudentViewSet, basename='excellent-student')
router.register('interview-questions', InterviewQuestionViewSet, basename='interview-question')

urlpatterns = [
    path('', include(router.urls)),
]
