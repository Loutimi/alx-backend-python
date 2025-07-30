from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


def homepage(request):
    return render(request, 'homepage.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def delete_user(request, id):
    user_to_delete = get_object_or_404(User, id=id)

    # Only allow users to delete themselves, or admins to delete anyone
    if request.user != user_to_delete and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this user.")

    # Only allow deletion via POST
    if request.method == "POST":
        user_to_delete.delete()
        messages.success(request, "User deleted successfully.")

        # If the current user deleted themselves, log them out
        if user_to_delete == request.user:
            logout(request)
            return redirect('homepage')  # Redirect to homepage after self-deletion

        return redirect('homepage')  # Redirect to homepage
    else:
        return render(request, 'messaging/confirm_delete.html', {'user_to_delete': user_to_delete})
