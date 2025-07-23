from rest_framework import viewsets, status, filters  
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Only return conversations the user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        participants = self.request.data.get('participant_ids', [])
        if self.request.user.id not in participants:
            participants.append(self.request.user.id)
        conversation = serializer.save()
        conversation.participants.set(participants)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  
    filterset_fields = ['conversation']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Only messages from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender_id=self.request.user)
