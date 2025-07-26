from datetime import datetime, time
import logging
from django.http import JsonResponse


logger = logging.getLogger('user_requests')

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
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
        end_time = time(21, 0)    # 9:00 PM

        if not (start_time <= current_time <= end_time):
            return JsonResponse({'error': 'Access is only allowed between 6 PM and 9 PM'}, status=403)
        return self.get_response(request)
