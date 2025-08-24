from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target_object):
    """
    Create a notification
    
    Args:
        recipient: User who will receive the notification
        actor: User who performed the action
        verb: Action performed (liked, commented, followed)
        target_object: The object the action was performed on
    """
    # Don't create notification if user is acting on their own content
    if recipient == actor:
        return None
    
    # Get the content type of the target object
    target_content_type = ContentType.objects.get_for_model(target_object)
    
    # Check if notification already exists (to prevent duplicates)
    existing_notification = Notification.objects.filter(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=target_content_type,
        target_object_id=target_object.id
    ).first()
    
    if existing_notification:
        # Update timestamp if notification already exists
        existing_notification.read = False
        existing_notification.save()
        return existing_notification
    
    # Create new notification
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=target_content_type,
        target_object_id=target_object.id
    )
    
    return notification