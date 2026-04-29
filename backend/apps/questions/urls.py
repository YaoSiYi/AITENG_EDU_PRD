from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, QuestionCategoryViewSet, WrongQuestionViewSet, AssignmentViewSet

router = DefaultRouter()
router.register('', QuestionViewSet, basename='question')
router.register('categories', QuestionCategoryViewSet, basename='category')
router.register('wrong', WrongQuestionViewSet, basename='wrong-question')
router.register('assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
