from django.contrib import admin
from .models import TestCase


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['public_id', 'title', 'product', 'module', 'priority', 'status', 'stage', 'creator', 'created_at']
    list_filter = ['priority', 'status', 'stage', 'product', 'module']
    search_fields = ['title', 'description', 'product', 'module', 'test_point']
    readonly_fields = ['public_id', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('public_id', 'title', 'description')
        }),
        ('分类信息', {
            'fields': ('product', 'module', 'sub_module', 'test_point')
        }),
        ('测试内容', {
            'fields': ('precondition', 'steps', 'expected_result', 'actual_result')
        }),
        ('属性', {
            'fields': ('priority', 'status', 'stage', 'case_type', 'remark')
        }),
        ('审计信息', {
            'fields': ('creator', 'updater', 'created_at', 'updated_at')
        }),
    )
