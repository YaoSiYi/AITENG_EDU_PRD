from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.utils import timezone
import random
from .models import Question, QuestionCategory, WrongQuestion, Assignment, UserAssignment
from .serializers import (
    QuestionSerializer, QuestionCategorySerializer, WrongQuestionSerializer,
    AssignmentSerializer, UserAssignmentSerializer
)


class QuestionViewSet(viewsets.ModelViewSet):
    """题库视图集"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = ['stage', 'subject', 'difficulty']
    search_fields = ['content', 'subject']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def random(self, request):
        """随机获取题目"""
        stage = request.query_params.get('stage')
        count = int(request.query_params.get('count', 10))

        queryset = self.get_queryset()
        if stage:
            queryset = queryset.filter(stage=stage)

        questions = list(queryset)
        random_questions = random.sample(questions, min(count, len(questions)))
        serializer = self.get_serializer(random_questions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """按分类获取题目"""
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': '请提供分类ID'}, status=status.HTTP_400_BAD_REQUEST)

        questions = self.get_queryset().filter(category_id=category_id)
        page = self.paginate_queryset(questions)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class QuestionCategoryViewSet(viewsets.ModelViewSet):
    """题目分类视图集"""
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer
    permission_classes = [AllowAny]


class WrongQuestionViewSet(viewsets.ModelViewSet):
    """错题本视图集"""
    serializer_class = WrongQuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WrongQuestion.objects.filter(user=self.request.user, is_correct=False)

    @action(detail=True, methods=['post'])
    def mark_correct(self, request, pk=None):
        """标记为已掌握"""
        wrong_question = self.get_object()
        wrong_question.is_correct = True
        wrong_question.save()
        return Response({'message': '已从错题本移除'})

    @action(detail=False, methods=['post'])
    def add(self, request):
        """添加错题"""
        question_id = request.data.get('question_id')
        user_answer = request.data.get('user_answer', '')

        wrong_question, created = WrongQuestion.objects.get_or_create(
            user=request.user,
            question_id=question_id,
            defaults={'user_answer': user_answer}
        )

        if not created:
            wrong_question.attempt_count += 1
            wrong_question.user_answer = user_answer
            wrong_question.save()

        serializer = self.get_serializer(wrong_question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssignmentViewSet(viewsets.ModelViewSet):
    """作业视图集"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """提交作业"""
        assignment = self.get_object()
        answers = request.data.get('answers', {})

        # 计算得分
        correct_count = 0
        total_count = assignment.questions.count()

        for question_id, user_answer in answers.items():
            question = assignment.questions.filter(id=question_id).first()
            if question and question.answer == user_answer:
                correct_count += 1

        score = (correct_count / total_count * 100) if total_count > 0 else 0

        # 保存用户作业记录
        user_assignment, created = UserAssignment.objects.update_or_create(
            user=request.user,
            assignment=assignment,
            defaults={
                'score': score,
                'completed': True,
                'completed_at': timezone.now()
            }
        )

        return Response({
            'score': score,
            'correct_count': correct_count,
            'total_count': total_count
        })
