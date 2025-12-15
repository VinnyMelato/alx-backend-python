# middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
from time import time
import logging

# ------------------------
# Setup logger
# ------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(filename='requests.log', level=logging.INFO)

# ------------------------
# 1. Logging User Requests Middleware
# ------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', 'Anonymous')
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

# ------------------------
# 2. Restrict Chat Access by Time Middleware
# ------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Chat is unavailable between 9 PM and 6 AM
        if 21 <= current_hour or current_hour < 6:
            return HttpResponseForbidden("Chat is not available between 9 PM and 6 AM.")
        return self.get_response(request)

# ------------------------
# 3. Offensive Language / Rate Limiting Middleware
# ------------------------
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_tracker = {}

    def __call__(self, request):
        # Only track POST requests to /chat/ endpoint
        if request.method == "POST" and request.path.startswith("/chat/"):
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            now = time()
            messages = self.ip_message_tracker.get(ip, [])
            # Remove messages older than 60 seconds
            messages = [msg_time for msg_time in messages if now - msg_time < 60]
            if len(messages) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )
            messages.append(now)
            self.ip_message_tracker[ip] = messages
        return self.get_response(request)

# ------------------------
# 4. Role-Based Access Middleware
# ------------------------
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        # Example: Restrict admin actions
        if request.path.startswith("/admin-actions/") and not (user and user.is_authenticated and user.is_staff):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
