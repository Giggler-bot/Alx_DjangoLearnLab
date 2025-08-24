from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """List all notifications for the authenticated user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor').order_by('-timestamp')

class UnreadNotificationListView(generics.ListAPIView):
    """List only unread notifications for the authenticated user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            read=False
        ).select_related('actor').order_by('-timestamp')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.mark_as_read()
        return Response({
            'message': 'Notification marked as read',
            'notification_id': notification_id
        })
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications as read for the authenticated user"""
    count = Notification.objects.filter(
        recipient=request.user,
        read=False
    ).update(read=True)
    
    return Response({
        'message': f'{count} notifications marked as read'
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_count(request):
    """Get notification counts for the authenticated user"""
    total_count = Notification.objects.filter(recipient=request.user).count()
    unread_count = Notification.objects.filter(
        recipient=request.user,
        read=False
    ).count()
    
    return Response({
        'total_notifications': total_count,
        'unread_notifications': unread_count
    })