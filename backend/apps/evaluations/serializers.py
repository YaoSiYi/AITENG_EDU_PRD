from rest_framework import serializers
from .models import Evaluation, StudentProgress


class EvaluationSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.nickname', read_only=True)
    student_name = serializers.CharField(source='student.nickname', read_only=True)

    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['teacher']


class StudentProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nickname', read_only=True)
    teacher_name = serializers.CharField(source='teacher.nickname', read_only=True)
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = StudentProgress
        fields = '__all__'

    def get_completion_rate(self, obj):
        if obj.total_questions == 0:
            return 0
        return round(obj.completed_questions / obj.total_questions * 100, 2)
