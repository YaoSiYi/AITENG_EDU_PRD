from django.db import models
from django.conf import settings
from common.snowflake import generate_snowflake_id


class TestCase(models.Model):
    """测试用例模型"""

    class Priority(models.TextChoices):
        LOW = 'low', '低'
        MEDIUM = 'medium', '中'
        HIGH = 'high', '高'
        CRITICAL = 'critical', '紧急'

    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        ACTIVE = 'active', '有效'
        DEPRECATED = 'deprecated', '已废弃'

    # 对外公开 ID（雪花算法生成，避免直接暴露自增主键）
    public_id = models.BigIntegerField('公共ID', unique=True, default=generate_snowflake_id, editable=False)

    # 产品 / 功能维度
    product = models.CharField('产品', max_length=100, blank=True)
    module = models.CharField('功能模块', max_length=100, blank=True)
    sub_module = models.CharField('子模块', max_length=100, blank=True)
    test_point = models.CharField('测试点', max_length=200, blank=True)

    title = models.CharField('标题', max_length=200)
    description = models.TextField('描述', blank=True)
    precondition = models.TextField('前置条件', blank=True)
    # 测试步骤，可存 JSON 或纯文本，这里用 TextField 存多行步骤
    steps = models.TextField('测试步骤', blank=True, help_text='每行一个步骤')
    expected_result = models.TextField('预期结果', blank=True)
    actual_result = models.TextField('实际结果', blank=True)
    priority = models.CharField(
        '优先级',
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        '状态',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    is_smoke = models.BooleanField('是否为冒烟用例', default=False)
    case_type = models.CharField('用例类型', max_length=50, blank=True)
    remark = models.TextField('备注', blank=True)
    # 可选：关联创建人（若需要按用户隔离）
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='test_cases',
        verbose_name='创建人',
    )
    # 最近修改人
    updater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_test_cases',
        verbose_name='修改人',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例'

    def __str__(self):
        return self.title
