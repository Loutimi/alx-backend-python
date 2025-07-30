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


# Post_delete signal on the User model to delete all messages,
@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    # Delete messages where the user is sender or recipient
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(recipient=instance).delete()

    # Delete notifications related to user’s messages
    Notification.objects.filter(message__sender=instance).delete()
    Notification.objects.filter(message__recipient=instance).delete()

    # Delete message history related to the user’s messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__recipient=instance).delete()
