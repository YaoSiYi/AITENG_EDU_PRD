from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'phone', 'qq', 'wechat_openid',
                  'hometown', 'password_hint', 'period', 'study_status', 'avatar', 'role', 'gender', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    confirm_password = serializers.CharField(write_only=True, min_length=6, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'phone', 'qq',
                  'wechat_openid', 'nickname', 'hometown', 'password_hint', 'gender']

    def validate(self, attrs):
        # 验证两次密码是否一致
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "两次密码不一致"})

        # 至少需要一种登录方式
        if not any([attrs.get('phone'), attrs.get('qq'), attrs.get('wechat_openid')]):
            raise serializers.ValidationError("请至少提供一种登录方式(手机号/QQ/微信)")

        return attrs

    def create(self, validated_data):
        # 保存明文密码
        password = validated_data.get('password')
        validated_data['plain_password'] = password
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义JWT Token序列化器"""
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""
    class Meta:
        model = User
        fields = ['nickname', 'hometown', 'gender', 'password_hint', 'avatar']


class PasswordResetSerializer(serializers.Serializer):
    """密码重置序列化器"""
    phone = serializers.CharField(max_length=11)
    verification_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次密码不一致")
        return attrs
