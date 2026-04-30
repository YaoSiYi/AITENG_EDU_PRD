from django.contrib import admin
from django.utils.html import format_html
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """轮播图管理"""

    list_display = [
        'id',
        'title',
        'image_preview',
        'order',
        'status',
        'is_active_display',
        'start_time',
        'end_time',
        'created_at',
    ]

    list_filter = ['status', 'created_at']

    search_fields = ['title', 'link']

    list_editable = ['order', 'status']

    readonly_fields = ['image_preview', 'created_at', 'updated_at']

    fieldsets = [
        ('基本信息', {
            'fields': ['title', 'image', 'image_preview', 'link']
        }),
        ('显示设置', {
            'fields': ['order', 'status']
        }),
        ('时间设置', {
            'fields': ['start_time', 'end_time'],
            'description': '可以设置轮播图的显示时间范围，留空则不限制'
        }),
        ('系统信息', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def image_preview(self, obj):
        """图片预览"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 100px; border-radius: 4px;"/>',
                obj.image.url
            )
        return '-'
    image_preview.short_description = '图片预览'

    def status_display(self, obj):
        """状态显示"""
        colors = {
            'active': '#67C23A',
            'inactive': '#909399',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            colors.get(obj.status, '#909399'),
            obj.get_status_display()
        )
    status_display.short_description = '状态'

    def is_active_display(self, obj):
        """是否有效显示"""
        if obj.is_active:
            return format_html(
                '<span style="color: #67C23A; font-weight: bold;">✓ 有效</span>'
            )
        return format_html(
            '<span style="color: #F56C6C; font-weight: bold;">✗ 无效</span>'
        )
    is_active_display.short_description = '当前状态'

    def save_model(self, request, obj, form, change):
        """保存时的额外处理"""
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ['admin/css/custom_admin.css']
        }
