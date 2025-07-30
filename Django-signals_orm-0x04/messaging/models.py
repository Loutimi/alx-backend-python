from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} sent a message to {self.receiver.username} at {self.timestamp}"


class Notification(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="notifications"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.receiver.username} - Read: {self.is_read}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="history"
    )
    edited_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Edit for Message ID {self.message.id} at {self.edited_at}"
