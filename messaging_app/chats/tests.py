from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from chats.models import Conversation, Message

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='password123',
            role='guest'
        )
        self.assertEqual(str(user), 'testuser (guest)')
        self.assertTrue(user.user_id)  # UUID assigned

class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', first_name='U1', last_name='One', email='u1@example.com', password='pass', role='guest'
        )
        self.user2 = User.objects.create_user(
            username='user2', first_name='U2', last_name='Two', email='u2@example.com', password='pass', role='host'
        )

    def test_create_conversation(self):
        conv = Conversation.objects.create()
        conv.participants.set([self.user1, self.user2])
        self.assertEqual(conv.participants.count(), 2)
        self.assertIn(self.user1, conv.participants.all())
        self.assertIn(self.user2, conv.participants.all())
        self.assertTrue(str(conv).startswith('Conversation'))

class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', first_name='U1', last_name='One', email='u1@example.com', password='pass', role='guest'
        )
        self.user2 = User.objects.create_user(
            username='user2', first_name='U2', last_name='Two', email='u2@example.com', password='pass', role='host'
        )
        self.conv = Conversation.objects.create()
        self.conv.participants.set([self.user1, self.user2])

    def test_create_message(self):
        msg = Message.objects.create(sender=self.user1, conversation=self.conv, message_body='Hello!')
        self.assertEqual(str(msg).split()[1], self.user1.username)  # "From user1 at ..."
        self.assertEqual(msg.message_body, 'Hello!')
