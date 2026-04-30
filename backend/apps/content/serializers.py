from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """轮播图序列化器"""

    image_url = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Banner
        fields = [
            'id',
            'title',
            'image',
            'image_url',
            'link',
            'order',
            'status',
            'is_active',
            'start_time',
            'end_time',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def get_image_url(self, obj):
        """获取图片完整URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
