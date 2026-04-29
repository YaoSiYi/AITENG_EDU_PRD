from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Evaluation(models.Model):
    """评价模型"""
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_evaluations',
        verbose_name='老师'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_evaluations',
        verbose_name='学员'
    )
    content = models.TextField('评价内容')
    rating = models.IntegerField('评分', default=5)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'evaluations'
        verbose_name = '评价'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.teacher.nickname} 评价 {self.student.nickname}"


class StudentProgress(models.Model):
    """学员进度"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='学员')
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_students',
        verbose_name='负责老师'
    )
    total_questions = models.IntegerField('总题数', default=0)
    completed_questions = models.IntegerField('已完成题数', default=0)
    correct_rate = models.FloatField('正确率', default=0.0)
    study_hours = models.FloatField('学习时长(小时)', default=0.0)
    last_study_time = models.DateTimeField('最后学习时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'student_progress'
        verbose_name = '学员进度'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.student.nickname} - 进度 {self.completed_questions}/{self.total_questions}"
