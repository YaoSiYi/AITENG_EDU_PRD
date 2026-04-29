from rest_framework import serializers

from .models import Dormitory, EmploymentStats, ExcellentStudent, InterviewQuestion, StudentStats


class StudentStatsSerializer(serializers.ModelSerializer):
    """学员统计序列化器"""
    class Meta:
        model = StudentStats
        fields = '__all__'


class DormitorySerializer(serializers.ModelSerializer):
    """宿舍管理序列化器"""
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = Dormitory
        fields = ['id', 'student', 'student_name', 'gender', 'gender_display',
                  'period', 'hometown', 'dormitory', 'phone', 'created_at', 'updated_at']

    def get_gender_display(self, obj):
        """获取性别显示名称"""
        return obj.get_gender_display() if obj.gender else ''


class EmploymentStatsSerializer(serializers.ModelSerializer):
    """就业统计序列化器"""
    salary_k = serializers.SerializerMethodField()
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = EmploymentStats
        fields = ['id', 'student', 'student_name', 'period', 'gender', 'gender_display',
                  'company', 'position', 'salary', 'salary_k', 'city', 'created_at']

    def get_salary_k(self, obj):
        """将薪资转换为 K 格式"""
        return f"{int(obj.salary / 1000)}K"

    def get_gender_display(self, obj):
        """获取性别显示名称"""
        return obj.get_gender_display() if obj.gender else ''


class EmploymentStatsListSerializer(serializers.ModelSerializer):
    """就业统计列表序列化器（含期数和性别）"""
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = EmploymentStats
        fields = ['id', 'period', 'gender', 'gender_display', 'student_name',
                  'company', 'position', 'city', 'salary', 'created_at']

    def get_gender_display(self, obj):
        """获取性别显示名称"""
        return obj.get_gender_display() if obj.gender else ''


class ExcellentStudentSerializer(serializers.ModelSerializer):
    """优秀学员序列化器"""
    salary = serializers.SerializerMethodField()

    class Meta:
        model = ExcellentStudent
        fields = ['id', 'name', 'avatar', 'company', 'salary', 'position', 'testimonial']

    def get_salary(self, obj):
        """将薪资转换为 K 格式"""
        return f"{int(obj.salary / 1000)}K"


class InterviewQuestionSerializer(serializers.ModelSerializer):
    """面试题序列化器"""
    class Meta:
        model = InterviewQuestion
        fields = '__all__'
