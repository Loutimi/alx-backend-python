from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Notification, Message, MessageHistory
from django.contrib.auth.models import User


# Create a notification once a message is created
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, receiver=instance.receiver)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    edited_content=old_message.content,
                    edited_by=old_message.sender,
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """
    Deletes all messages, notifications, and message histories associated with a user
    when the user is deleted.
    """

    # Fetch all message IDs sent or received by the user
    messages = Message.objects.filter(sender=instance) | Message.objects.filter(recipient=instance)
    message_ids = messages.values_list("id", flat=True)

    # Delete message history linked to these messages
    MessageHistory.objects.filter(message_id__in=message_ids).delete()

    # Delete notifications linked to these messages
    Notification.objects.filter(message_id__in=message_ids).delete()

    # Delete the messages themselves
    messages.delete()
