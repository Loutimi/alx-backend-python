from rest_framework import viewsets, status, filters  
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend  
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Show only conversations where the user is a participant
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participants=[self.request.user])  # auto-add creator


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        return Message.objects.filter(conversation__id=conversation_id, conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_pk")
        serializer.save(sender=self.request.user, conversation_id=conversation_id)
