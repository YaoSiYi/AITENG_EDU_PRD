from django.contrib import admin
from .models import TestCase


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'creator', 'created_at', 'updated_at')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'steps', 'expected_result')}),
        ('分类', {'fields': ('priority', 'status')}),
        ('关联', {'fields': ('creator',)}),
        ('时间', {'fields': ('created_at', 'updated_at')}),
    )
