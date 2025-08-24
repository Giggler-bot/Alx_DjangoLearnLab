from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    VERB_CHOICES = [
        ('liked', 'liked your post'),
        ('commented', 'commented on your post'),
        ('followed', 'started following you'),
        ('mentioned', 'mentioned you in a post'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=20, choices=VERB_CHOICES)
    
    # Generic foreign key to link to any model (Post, Comment, etc.)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', '-timestamp']),
            models.Index(fields=['read', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.actor.username} {self.get_verb_display()}"

    def mark_as_read(self):
        """Mark notification as read"""
        self.read = True
        self.save()

    @property
    def message(self):
        """Generate a human-readable message"""
        return f"{self.actor.username} {self.get_verb_display()}"