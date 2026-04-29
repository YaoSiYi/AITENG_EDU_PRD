from rest_framework import serializers
from .models import Question, QuestionCategory, WrongQuestion, Assignment, UserAssignment


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class WrongQuestionSerializer(serializers.ModelSerializer):
    question_detail = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = WrongQuestion
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    questions_detail = QuestionSerializer(source='questions', many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'


class UserAssignmentSerializer(serializers.ModelSerializer):
    assignment_detail = AssignmentSerializer(source='assignment', read_only=True)

    class Meta:
        model = UserAssignment
        fields = '__all__'
