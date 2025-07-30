from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Message
from django.db.models import Prefetch


def homepage(request):
    return render(request, "homepage.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    # Allow if the user is deleting themselves OR the user is staff
    if request.user != user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this user.")

    user.delete()
    return redirect("homepage")


def conversation_thread(request, user_id):
    messages = (
        Message.objects
        .filter(
            sender=request.user,
            recipient_id=user_id,
            parent_message__isnull=True  # top-level messages only
        )
        .select_related('sender', 'recipient')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'recipient'))
        )
        .order_by('-timestamp')
    )
    return render(request, 'messaging/threaded_conversation.html', {'messages': messages})
