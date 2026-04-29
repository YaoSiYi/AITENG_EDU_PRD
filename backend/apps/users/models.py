from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户模型"""
    ROLE_CHOICES = [
        ('guest', '游客'),
        ('student', '学生'),
        ('teacher', '老师'),
        ('admin', '管理员'),
    ]

    STUDY_STATUS_CHOICES = [
        ('studying', '在读'),
        ('graduated', '毕业'),
    ]

    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    qq = models.CharField('QQ号', max_length=20, null=True, blank=True)
    wechat_openid = models.CharField('微信OpenID', max_length=100, null=True, blank=True)
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    hometown = models.CharField('籍贯', max_length=100, blank=True, default='', help_text='格式：xx省xx市')
    password_hint = models.CharField('密码提示', max_length=200, blank=True, default='', help_text='用于找回密码的提示信息')
    period = models.CharField('期数', max_length=50, blank=True, default='', help_text='格式：xxxx-xx-xx期学员，例如：2024-01-01期学员')
    study_status = models.CharField('学习状态', max_length=20, choices=STUDY_STATUS_CHOICES, default='studying', help_text='学员的学习状态：在读或毕业')
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='student')
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, blank=True, default='', help_text='性别：男或女')
    plain_password = models.CharField('明文密码', max_length=128, blank=True, default='', help_text='用于管理后台显示和修改密码')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname or self.username

    def save(self, *args, **kwargs):
        # 如果明文密码存在，同步更新哈希密码
        if self.plain_password:
            # 检查密码哈希是否与明文密码匹配
            if not self.pk or self._password_changed() or not self.check_password(self.plain_password):
                self.set_password(self.plain_password)
        super().save(*args, **kwargs)

    def _password_changed(self):
        """检查明文密码是否被修改"""
        if not self.pk:
            return True
        try:
            old_user = User.objects.get(pk=self.pk)
            return old_user.plain_password != self.plain_password
        except User.DoesNotExist:
            return True
