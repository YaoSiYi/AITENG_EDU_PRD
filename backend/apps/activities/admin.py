from django.contrib import admin
from .models import Activity, ActivityParticipant


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'is_active', 'start_time', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']


@admin.register(ActivityParticipant)
class ActivityParticipantAdmin(admin.ModelAdmin):
    list_display = ['activity', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['activity__title', 'user__nickname']
