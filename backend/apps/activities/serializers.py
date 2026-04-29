from rest_framework import serializers
from .models import Activity, ActivityParticipant


class ActivitySerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.nickname', read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['creator']

    def get_participant_count(self, obj):
        return obj.participants.count()


class ActivityParticipantSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.nickname', read_only=True)
    activity_title = serializers.CharField(source='activity.title', read_only=True)

    class Meta:
        model = ActivityParticipant
        fields = '__all__'
