from rest_framework import serializers
from django.contrib.auth.models import User


# 用户列表序列号
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
    
  def to_representation(self, instance):
    representation = super().to_representation(instance)
    # 添加public_id到序列化输出
    if hasattr(instance, 'profile'):
        representation['public_id'] = str(instance.profile.public_id)
    return representation