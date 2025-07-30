from datetime import datetime, time
import logging
from django.http import JsonResponse


logger = logging.getLogger("user_requests")


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = (
            request.user.username
            if hasattr(request, "user") and request.user.is_authenticated
            else "Anonymous"
        )
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = request.path

        logger.info(f"[{timestamp}] User: {user} - Path: {path}")

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()

        # Access window: 6 PM to 9 PM
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)  # 9:00 PM

        if not (start_time <= current_time <= end_time):
            return JsonResponse(
                {"error": "Access is only allowed between 6 PM and 9 PM"}, status=403
            )
        return self.get_response(request)


class OffensiveLanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # Structure: {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            current_time = time.time()
            time_window = 60  # 1 minute
            max_messages = 5

            # Get or initialize IP log
            message_times = self.message_log.get(ip, [])

            # Remove timestamps older than 60 seconds
            message_times = [t for t in message_times if current_time - t < time_window]

            if len(message_times) >= max_messages:
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded. Maximum 5 messages per minute allowed."
                    },
                    status=429,
                )

            # Log current message time
            message_times.append(current_time)
            self.message_log[ip] = message_times

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve client's IP address considering proxy headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bypass if not targeting restricted methods
        if request.method in ["DELETE", "PUT", "PATCH"]:
            user = request.user
            if not user.is_authenticated or not (user.is_superuser or user.is_staff):
                return JsonResponse(
                    {"error": "Access is only allowed for admin or moderator"},
                    status=403,
                )
        return self.get_response(request)
