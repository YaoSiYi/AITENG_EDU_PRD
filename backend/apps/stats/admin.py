from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Dormitory, EmploymentStats, ExcellentStudent, InterviewQuestion, StudentStats

User = get_user_model()


# 注释掉 StudentStats 的注册，避免与学员统计代理模型冲突
# @admin.register(StudentStats)
# class StudentStatsAdmin(admin.ModelAdmin):
#     """学员统计管理"""
#     list_display = ['period', 'province', 'city', 'count', 'created_at']
#     list_filter = ['period', 'province', 'created_at']
#     search_fields = ['period', 'province', 'city']
#     ordering = ['-created_at']


@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    """宿舍管理"""
    list_display = ['student_name', 'get_student_link', 'gender', 'period', 'hometown', 'dormitory', 'phone', 'updated_at']
    list_filter = ['gender', 'period', 'dormitory', 'updated_at']
    search_fields = ['student_name', 'dormitory', 'phone', 'hometown', 'student__username', 'student__nickname']
    ordering = ['dormitory', 'student_name']
    autocomplete_fields = ['student']

    fieldsets = (
        ('学员信息', {
            'fields': ('student', 'student_name', 'gender', 'period', 'hometown', 'phone')
        }),
        ('宿舍信息', {
            'fields': ('dormitory',)
        }),
    )

    readonly_fields = ['student_name', 'gender', 'period', 'hometown', 'phone']

    def get_student_link(self, obj):
        """显示关联用户的链接"""
        if obj.student:
            from django.urls import reverse
            from django.utils.html import format_html
            url = reverse('admin:users_user_change', args=[obj.student.id])
            return format_html('<a href="{}">{}</a>', url, obj.student.nickname or obj.student.username)
        return '-'
    get_student_link.short_description = '关联用户'

    def get_gender_display_custom(self, obj):
        """显示性别"""
        return obj.get_gender_display() if obj.gender else '-'
    get_gender_display_custom.short_description = '性别'


@admin.register(EmploymentStats)
class EmploymentStatsAdmin(admin.ModelAdmin):
    """就业统计管理"""
    list_display = ['student_name', 'get_student_link', 'period', 'gender', 'company', 'position', 'salary', 'city', 'created_at']
    list_filter = ['period', 'gender', 'city', 'created_at']
    search_fields = ['student_name', 'company', 'position', 'student__username', 'student__nickname']
    ordering = ['-salary']
    autocomplete_fields = ['student']

    fieldsets = (
        ('学员信息', {
            'fields': ('student', 'student_name', 'period', 'gender')
        }),
        ('就业信息', {
            'fields': ('company', 'position', 'salary', 'city')
        }),
    )

    def get_student_link(self, obj):
        """显示关联用户的链接"""
        if obj.student:
            from django.urls import reverse
            from django.utils.html import format_html
            url = reverse('admin:users_user_change', args=[obj.student.id])
            return format_html('<a href="{}">{}</a>', url, obj.student.nickname or obj.student.username)
        return '-'
    get_student_link.short_description = '关联用户'

    def get_gender_display(self, obj):
        """显示性别"""
        return obj.get_gender_display() if obj.gender else '-'
    get_gender_display.short_description = '性别'


@admin.register(ExcellentStudent)
class ExcellentStudentAdmin(admin.ModelAdmin):
    """优秀学员管理"""
    list_display = ['name', 'period', 'company', 'position', 'salary', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'period', 'created_at']
    search_fields = ['name', 'company', 'position']
    ordering = ['-created_at']
    list_editable = ['is_featured']


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    """面试题管理"""
    list_display = ['question_preview', 'category', 'frequency', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['question', 'answer', 'category']
    ordering = ['-frequency']

    def question_preview(self, obj):
        """问题预览"""
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = '问题'


# 自定义学员统计视图
class StudentStatisticsAdmin(admin.ModelAdmin):
    """学员统计视图（统计所有学生角色用户）"""
    change_list_template = 'admin/stats/student_statistics.html'

    def changelist_view(self, request, extra_context=None):
        """自定义列表视图"""
        # 统计所有学生角色的用户
        students = User.objects.filter(role='student').exclude(is_superuser=True)

        # 按期数统计
        period_stats = {}
        for student in students:
            period = student.period or '未分配期数'
            if period not in period_stats:
                period_stats[period] = {
                    'count': 0,
                    'studying': 0,
                    'graduated': 0,
                    'male': 0,
                    'female': 0,
                    'students': []
                }
            period_stats[period]['count'] += 1

            # 统计学习状态
            if student.study_status == 'studying':
                period_stats[period]['studying'] += 1
            else:
                period_stats[period]['graduated'] += 1

            # 统计性别
            if student.gender == 'male':
                period_stats[period]['male'] += 1
            elif student.gender == 'female':
                period_stats[period]['female'] += 1

            period_stats[period]['students'].append({
                'id': student.id,
                'username': student.username,
                'nickname': student.nickname,
                'phone': student.phone,
                'hometown': student.hometown,
                'gender': student.get_gender_display() if student.gender else '未填写',
                'study_status': student.study_status,
                'study_status_display': student.get_study_status_display(),
                'created_at': student.created_at,
            })

        # 总体统计
        total_students = students.count()
        studying_students = students.filter(study_status='studying').count()
        graduated_students = students.filter(study_status='graduated').count()
        male_students = students.filter(gender='male').count()
        female_students = students.filter(gender='female').count()

        # 按籍贯统计
        hometown_stats = {}
        for student in students:
            hometown = student.hometown or '未填写'
            hometown_stats[hometown] = hometown_stats.get(hometown, 0) + 1

        # 按创建时间统计（最近30天）
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_students = students.filter(created_at__gte=thirty_days_ago).count()

        extra_context = extra_context or {}
        extra_context.update({
            'title': '学员统计',
            'total_students': total_students,
            'studying_students': studying_students,
            'graduated_students': graduated_students,
            'male_students': male_students,
            'female_students': female_students,
            'period_stats': sorted(period_stats.items(), key=lambda x: x[1]['count'], reverse=True),
            'hometown_stats': sorted(hometown_stats.items(), key=lambda x: x[1], reverse=True)[:10],
            'recent_students': recent_students,
        })

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        """禁用添加功能"""
        return False

    def has_delete_permission(self, request, obj=None):
        """禁用删除功能"""
        return False


# 注册学员统计视图（使用代理模型）
class StudentStatisticsProxy(User):
    """学员统计代理模型"""
    class Meta:
        proxy = True
        verbose_name = '学员统计'
        verbose_name_plural = '学员统计'


admin.site.register(StudentStatisticsProxy, StudentStatisticsAdmin)
