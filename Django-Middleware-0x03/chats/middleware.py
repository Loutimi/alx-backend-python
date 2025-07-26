from datetime import datetime
import logging

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
