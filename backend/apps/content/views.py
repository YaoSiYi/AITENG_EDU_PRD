from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from .models import Banner
from .serializers import BannerSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """轮播图视图集（只读）"""

    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']

    def get_queryset(self):
        """只返回有效的轮播图"""
        queryset = super().get_queryset()
        now = timezone.now()

        # 过滤状态为active的
        queryset = queryset.filter(status='active')

        # 过滤时间范围内的
        queryset = queryset.filter(
            models.Q(start_time__isnull=True) | models.Q(start_time__lte=now)
        ).filter(
            models.Q(end_time__isnull=True) | models.Q(end_time__gte=now)
        )

        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取所有有效的轮播图"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
