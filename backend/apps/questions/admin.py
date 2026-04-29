from django.contrib import admin
from .models import Question, QuestionCategory, WrongQuestion, Assignment, UserAssignment


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['content', 'stage', 'subject', 'difficulty', 'created_at']
    list_filter = ['stage', 'subject', 'difficulty']
    search_fields = ['content', 'subject']


@admin.register(WrongQuestion)
class WrongQuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_correct', 'attempt_count', 'created_at']
    list_filter = ['is_correct']
    search_fields = ['user__nickname', 'question__content']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'stage', 'question_count', 'created_by', 'created_at']
    list_filter = ['stage']
    search_fields = ['title']


@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'assignment', 'score', 'completed', 'completed_at']
    list_filter = ['completed']
    search_fields = ['user__nickname', 'assignment__title']
