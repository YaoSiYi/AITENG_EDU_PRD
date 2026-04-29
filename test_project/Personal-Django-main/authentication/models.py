import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    用户配置文件模型，用于扩展Django内置的User模型
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 使用UUID作为公开的用户ID
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # Google 验证器 (TOTP)：密钥（base32），仅开启 2FA 后存在
    totp_secret = models.CharField(max_length=32, blank=True)
    # 是否已开启双因素认证
    totp_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.public_id}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当创建User时自动创建对应的UserProfile
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    保存User时同时保存UserProfile
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # 如果用户已经存在但没有profile，则创建一个
        UserProfile.objects.get_or_create(user=instance)