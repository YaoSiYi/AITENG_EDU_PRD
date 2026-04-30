from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Banner(models.Model):
    """轮播图模型"""

    STATUS_CHOICES = [
        ('active', '启用'),
        ('inactive', '禁用'),
    ]

    title = models.CharField('标题', max_length=200)
    image = models.ImageField('图片', upload_to='banners/%Y/%m/')
    link = models.URLField('链接地址', blank=True, help_text='点击轮播图跳转的链接')
    order = models.IntegerField(
        '排序',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        help_text='数字越小越靠前'
    )
    status = models.CharField(
        '状态',
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    start_time = models.DateTimeField('开始时间', null=True, blank=True, help_text='留空则立即生效')
    end_time = models.DateTimeField('结束时间', null=True, blank=True, help_text='留空则永久有效')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        """判断轮播图是否在有效期内"""
        from django.utils import timezone
        now = timezone.now()

        if self.status != 'active':
            return False

        if self.start_time and now < self.start_time:
            return False

        if self.end_time and now > self.end_time:
            return False

        return True
