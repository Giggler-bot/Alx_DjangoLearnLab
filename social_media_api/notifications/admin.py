from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'verb', 'read', 'timestamp']
    list_filter = ['verb', 'read', 'timestamp']
    search_fields = ['recipient__username', 'actor__username']
    readonly_fields = ['timestamp']
    
    def mark_as_read(self, request, queryset):
        """Admin action to mark notifications as read"""
        count = queryset.update(read=True)
        self.message_user(request, f'{count} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    actions = [mark_as_read]