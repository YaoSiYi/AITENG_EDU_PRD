from django.contrib import admin
from .models import Evaluation, StudentProgress


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'student', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['teacher__nickname', 'student__nickname', 'content']


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'teacher', 'completed_questions', 'total_questions', 'correct_rate', 'last_study_time']
    list_filter = ['teacher']
    search_fields = ['student__nickname', 'teacher__nickname']
