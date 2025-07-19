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
    sender_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'created_at', 'messages']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')

        if len(participant_ids) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")

        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation
