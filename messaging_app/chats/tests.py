import pytest
from chats.models import User, Conversation, Message
from django.utils import timezone

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username="testuser",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="password123",
        role="guest"
    )
    assert user.username == "testuser"
    assert user.role == "guest"

@pytest.mark.django_db
def test_create_conversation():
    user1 = User.objects.create_user(username="user1", first_name="U1", last_name="One", email="u1@example.com", password="pass1", role="guest")
    user2 = User.objects.create_user(username="user2", first_name="U2", last_name="Two", email="u2@example.com", password="pass2", role="guest")
    
    conv = Conversation.objects.create()
    conv.participants.set([user1, user2])
    
    assert user1 in conv.participants.all()
    assert user2 in conv.participants.all()

@pytest.mark.django_db
def test_create_message():
    sender = User.objects.create_user(username="sender", first_name="S", last_name="Ender", email="sender@example.com", password="pass3", role="guest")
    conv = Conversation.objects.create()
    conv.participants.set([sender])
    
    msg = Message.objects.create(sender=sender, conversation=conv, message_body="Hello!", sent_at=timezone.now())
    
    assert msg.sender == sender
    assert msg.conversation == conv
    assert msg.message_body == "Hello!"
