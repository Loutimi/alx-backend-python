# Generated by Django 5.2.4 on 2025-07-23 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="sender_id",
            new_name="sender",
        ),
    ]
