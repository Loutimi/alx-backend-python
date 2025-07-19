from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show conversations the user is part of
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically include the requesting user as a participant
        participants = self.request.data.get('participant_ids', [])
        if self.request.user.id not in participants:
            participants.append(self.request.user.id)
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter messages by conversation if conversation_id is in query params
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return self.queryset.filter(conversation_id=conversation_id)
        return self.queryset.none()  # prevent exposing all messages

    def perform_create(self, serializer):
        serializer.save(sender_id=self.request.user)
