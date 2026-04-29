from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Evaluation, StudentProgress
from .serializers import EvaluationSerializer, StudentProgressSerializer

User = get_user_model()


class EvaluationViewSet(viewsets.ModelViewSet):
    """评价视图集"""
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Evaluation.objects.filter(teacher=user)
        elif user.role == 'student':
            return Evaluation.objects.filter(student=user)
        return Evaluation.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=False, methods=['get'])
    def my_evaluations(self, request):
        """获取我收到的评价"""
        evaluations = Evaluation.objects.filter(student=request.user)
        serializer = self.get_serializer(evaluations, many=True)
        return Response(serializer.data)


class StudentProgressViewSet(viewsets.ModelViewSet):
    """学员进度视图集"""
    serializer_class = StudentProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            # 老师查看自己负责的学员
            return StudentProgress.objects.filter(teacher=user)
        elif user.role == 'student':
            # 学生查看自己的进度
            return StudentProgress.objects.filter(student=user)
        return StudentProgress.objects.none()

    @action(detail=False, methods=['get'])
    def my_students(self, request):
        """老师查看名下学员列表"""
        if request.user.role != 'teacher':
            return Response(
                {'error': '只有老师可以查看学员列表'},
                status=status.HTTP_403_FORBIDDEN
            )

        students = StudentProgress.objects.filter(teacher=request.user)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """更新学员进度"""
        progress = self.get_object()

        # 只有负责老师可以更新
        if progress.teacher != request.user:
            return Response(
                {'error': '无权限更新此学员进度'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
