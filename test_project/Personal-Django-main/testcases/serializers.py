from rest_framework import serializers
from .models import TestCase


class TestCaseSerializer(serializers.ModelSerializer):
    """测试用例序列化器（列表与详情）。对外主 ID 为 public_id（雪花），响应中 id 即 public_id。"""

    id = serializers.SerializerMethodField(read_only=True)
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    updater_name = serializers.CharField(source='updater.username', read_only=True)

    def get_id(self, obj):
        """对外统一使用雪花 public_id 作为主 id（字符串，避免前端大数精度问题）"""
        return str(obj.public_id)

    class Meta:
        model = TestCase
        fields = [
            'id',
            'product',
            'module',
            'sub_module',
            'test_point',
            'title',
            'description',
            'precondition',
            'steps',
            'expected_result',
            'actual_result',
            'priority',
            'status',
            'is_smoke',
            'case_type',
            'remark',
            'creator',
            'creator_name',
            'updater',
            'updater_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'creator', 'updater', 'created_at', 'updated_at']


class TestCaseCreateUpdateSerializer(serializers.ModelSerializer):
    """创建/更新用的序列化器（可限制必填与校验）。支持用 name 作为 title 的别名。"""

    name = serializers.CharField(required=False, write_only=True, allow_blank=True)

    class Meta:
        model = TestCase
        fields = [
            'product',
            'module',
            'sub_module',
            'test_point',
            'title',
            'name',
            'description',
            'precondition',
            'steps',
            'expected_result',
            'actual_result',
            'priority',
            'status',
            'is_smoke',
            'case_type',
            'remark',
            'creator',
        ]

    def to_internal_value(self, data):
        # 前端可能传 name 而非 title，兼容：有 name 且 title 为空时用 name 作为 title
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        if data.get('title') in (None, ''):
            if data.get('name'):
                data['title'] = data['name']
        data.pop('name', None)
        return super().to_internal_value(data)

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('标题不能为空')
        return value.strip()
