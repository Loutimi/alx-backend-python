from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of the conversation or message.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated for all actions
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            # For Conversation objects
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # For Message objects
            return request.user in obj.conversation.participants.all()
        return False
