from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Activity(models.Model):
    """活动模型"""
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    title = models.CharField('活动标题', max_length=200)
    description = models.TextField('活动描述')
    form_data = models.JSONField('表单数据', default=dict, blank=True)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    is_active = models.BooleanField('是否激活', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'activities'
        verbose_name = '活动'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ActivityParticipant(models.Model):
    """活动参与者"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='参与者')
    form_data = models.JSONField('提交数据', default=dict, blank=True)
    created_at = models.DateTimeField('参与时间', auto_now_add=True)

    class Meta:
        db_table = 'activity_participants'
        verbose_name = '活动参与者'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['activity', 'user'], name='unique_activity_user')
        ]

    def __str__(self):
        return f"{self.user.nickname} - {self.activity.title}"
