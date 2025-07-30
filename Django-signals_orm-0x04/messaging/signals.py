from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Notification, Message, MessageHistory


# Create a notification once a message is created
@receiver(post_save, sender=Message)
def create_or_save_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=instance,
            receiver=instance.receiver
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    edited_content=old_message.content,
                    edited_by=old_message.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
