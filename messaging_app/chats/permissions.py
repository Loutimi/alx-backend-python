from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow users to access conversations or messages
    where they are participants.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            # For Conversation objects
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # For Message objects
            return request.user in obj.conversation.participants.all()
        return False
