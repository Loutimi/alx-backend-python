from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(max_length=1000)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    participant_ids = serializers.ListField(
        write_only=True,
        child=serializers.UUIDField()
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'created_at']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        users = User.objects.filter(user_id__in=participant_ids)

        if users.count() != len(participant_ids):
            raise serializers.ValidationError("One or more participant_ids are invalid.")

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        return conversation
