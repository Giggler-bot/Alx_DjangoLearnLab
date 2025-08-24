from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    message = serializers.ReadOnlyField()
    target_info = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'message', 'target_info', 'read', 'timestamp']
        read_only_fields = ['id', 'actor', 'verb', 'message', 'target_info', 'timestamp']

    def get_target_info(self, obj):
        """Get information about the target object"""
        if hasattr(obj.target, 'title'):  # Post
            return {
                'type': 'post',
                'id': obj.target.id,
                'title': obj.target.title
            }
        elif hasattr(obj.target, 'content') and hasattr(obj.target, 'post'):  # Comment
            return {
                'type': 'comment',
                'id': obj.target.id,
                'post_title': obj.target.post.title
            }
        elif hasattr(obj.target, 'username'):  # User (for follows)
            return {
                'type': 'user',
                'id': obj.target.id,
                'username': obj.target.username
            }
        return None