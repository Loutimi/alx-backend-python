from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Message


# Create a notification once a message is created
@receiver(post_save, sender=Message)
def create_or_save_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=instance,
            receiver=instance.receiver
        )
