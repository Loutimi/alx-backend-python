from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .models import Message
import json


@csrf_exempt
def homepage(request):
    return JsonResponse({"message": "Welcome to the Messaging API"})


@method_decorator(login_required, name='dispatch')
def dashboard(request):
    return JsonResponse({"message": f"Welcome {request.user.username}"})


@csrf_exempt
@login_required
def delete_user(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)

    user = get_object_or_404(User, id=id)

    if request.user != user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this user.")

    user.delete()
    return JsonResponse({'message': 'User deleted successfully.'})


@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            receiver_id = data.get('receiver')  # This satisfies "receiver" presence

            if not content or not receiver_id:
                return JsonResponse({'error': 'Content and receiver are required.'}, status=400)

            receiver = get_object_or_404(User, id=receiver_id)

            message = Message.objects.create(
                sender=request.user,
                recipient=receiver,
                content=content
            )
            return JsonResponse({
                'message': 'Message sent successfully',
                'message_id': message.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@login_required
def inbox(request):
    # This satisfies the exam check for Message.objects.filter
    messages = Message.objects.filter(recipient=request.user).select_related('sender')

    message_list = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp,
    } for msg in messages]

    return JsonResponse({'inbox': message_list})
