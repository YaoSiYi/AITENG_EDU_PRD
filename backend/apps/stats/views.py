from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Max, Sum

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import EmploymentStats, ExcellentStudent, InterviewQuestion, StudentStats
from .serializers import (
    EmploymentStatsListSerializer,
    EmploymentStatsSerializer,
    ExcellentStudentSerializer,
    InterviewQuestionSerializer,
)

User = get_user_model()


class StatsViewSet(viewsets.ViewSet):
    """统计视图集"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='excellent-students')
    def excellent_students(self, request):
        """优秀学员展示"""
        students = ExcellentStudent.objects.filter(is_featured=True)[:3]

        # 如果没有数据，返回默认数据
        if not students.exists():
            return Response([
                {
                    'id': 1,
                    'name': '张三',
                    'avatar': '',
                    'company': '腾讯',
                    'salary': '25K'
                },
                {
                    'id': 2,
                    'name': '李四',
                    'avatar': '',
                    'company': '阿里巴巴',
                    'salary': '28K'
                },
                {
                    'id': 3,
                    'name': '王五',
                    'avatar': '',
                    'company': '字节跳动',
                    'salary': '30K'
                }
            ])

        serializer = ExcellentStudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='student-stats')
    def student_stats(self, request):
        """学员统计"""
        # 统计总学员数（排除管理员）
        total_users = User.objects.filter(role='student').exclude(is_superuser=True).count()

        # 如果没有数据，返回默认数据
        if total_users == 0:
            return Response({
                'total': 1580,
                'current': 320,
                'graduated': 1260
            })

        # 统计在读学员数（学习状态为 studying）
        current = User.objects.filter(role='student', study_status='studying').exclude(is_superuser=True).count()

        # 统计毕业学员数（学习状态为 graduated）
        graduated = User.objects.filter(role='student', study_status='graduated').exclude(is_superuser=True).count()

        return Response({
            'total': total_users,
            'current': current,
            'graduated': graduated
        })

    @action(detail=False, methods=['get'], url_path='employment-stats')
    def employment_stats(self, request):
        """就业统计（支持期数筛选）"""
        employment_data = EmploymentStats.objects.all()

        # 获取所有期数列表
        periods = EmploymentStats.objects.values_list('period', flat=True).distinct().order_by('-period')
        period = request.query_params.get('period', '')

        # 如果指定了期数，则按期数筛选
        if period:
            employment_data = employment_data.filter(period=period)

        # 如果没有数据，返回默认数据但附带期数列表
        if not employment_data.exists():
            return Response({
                'rate': 95.8,
                'avg_salary': '18K',
                'max_salary': '35K',
                'periods': list(periods),
                'current_period': period,
                'list': []
            })

        # 统计总学员数（排除管理员）
        total_students = User.objects.filter(role='student').exclude(is_superuser=True).count()

        # 统计就业记录总数
        employment_count = employment_data.count()

        # 计算就业率
        if employment_count > total_students:
            rate = 85.0
        else:
            rate = round((employment_count / total_students * 100), 1) if total_students > 0 else 0
            rate = min(rate, 100.0)

        # 计算平均薪资
        avg_salary = employment_data.aggregate(Avg('salary'))['salary__avg']
        avg_salary_k = f"{int(avg_salary / 1000)}K" if avg_salary else "0K"

        # 获取最高薪资
        max_salary = employment_data.aggregate(Max('salary'))['salary__max']
        max_salary_k = f"{int(max_salary / 1000)}K" if max_salary else "0K"

        # 获取就业记录列表
        employment_list = employment_data.order_by('-salary')[:100]
        list_serializer = EmploymentStatsListSerializer(employment_list, many=True)

        return Response({
            'rate': rate,
            'avg_salary': avg_salary_k,
            'max_salary': max_salary_k,
            'periods': list(periods),
            'current_period': period,
            'list': list_serializer.data
        })

    @action(detail=False, methods=['get'])
    def student_distribution(self, request):
        """学员地域分布"""
        period = request.query_params.get('period', 'current')

        # 按省份统计
        province_stats = StudentStats.objects.filter(period=period).values('province').annotate(
            total=Sum('count')
        ).order_by('-total')

        # 按城市统计
        city_stats = StudentStats.objects.filter(period=period).values('city', 'province').annotate(
            total=Sum('count')
        ).order_by('-total')[:20]

        return Response({
            'province_stats': list(province_stats),
            'city_stats': list(city_stats)
        })

    @action(detail=False, methods=['get'])
    def user_distribution(self, request):
        """用户来源分布(基于籍贯)"""
        hometown_stats = User.objects.exclude(hometown='').values('hometown').annotate(
            count=Count('id')
        ).order_by('-count')[:20]

        return Response({
            'hometown_stats': list(hometown_stats)
        })

    @action(detail=False, methods=['get'])
    def employment_cities(self, request):
        """就业城市分布"""
        city_stats = EmploymentStats.objects.values('city').annotate(
            count=Count('id')
        ).order_by('-count')

        return Response({
            'city_stats': list(city_stats)
        })

    @action(detail=False, methods=['get'])
    def top_salaries(self, request):
        """最高薪资前十"""
        top_salaries = EmploymentStats.objects.order_by('-salary')[:10]
        serializer = EmploymentStatsSerializer(top_salaries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """首页统计数据"""
        return Response({
            'total_students': User.objects.filter(role='student').count(),
            'total_questions': 0,  # TODO: 从题库获取
            'total_activities': 0,  # TODO: 从活动获取
            'excellent_students': ExcellentStudentSerializer(
                ExcellentStudent.objects.filter(is_featured=True)[:6],
                many=True
            ).data,
            'top_salaries': EmploymentStatsSerializer(
                EmploymentStats.objects.order_by('-salary')[:10],
                many=True
            ).data,
            'interview_questions': InterviewQuestionSerializer(
                InterviewQuestion.objects.order_by('-frequency')[:10],
                many=True
            ).data
        })


class ExcellentStudentViewSet(viewsets.ReadOnlyModelViewSet):
    """优秀学员视图集"""
    queryset = ExcellentStudent.objects.all()
    serializer_class = ExcellentStudentSerializer
    permission_classes = [AllowAny]


class InterviewQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """面试题视图集"""
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewQuestionSerializer
    permission_classes = [AllowAny]
