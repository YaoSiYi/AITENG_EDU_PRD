from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Activity, ActivityParticipant
from .serializers import ActivitySerializer, ActivityParticipantSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """活动视图集"""
    queryset = Activity.objects.filter(is_active=True)
    serializer_class = ActivitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def participate(self, request, pk=None):
        """参与活动"""
        activity = self.get_object()
        form_data = request.data.get('form_data', {})

        participant, created = ActivityParticipant.objects.update_or_create(
            activity=activity,
            user=request.user,
            defaults={'form_data': form_data}
        )

        return Response({
            'message': '参与成功' if created else '更新成功',
            'data': ActivityParticipantSerializer(participant).data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """获取活动参与者列表"""
        activity = self.get_object()
        participants = activity.participants.all()
        serializer = ActivityParticipantSerializer(participants, many=True)
        return Response(serializer.data)
