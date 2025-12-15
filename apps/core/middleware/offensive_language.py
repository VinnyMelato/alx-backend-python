# offensive_language.py
from django.http import JsonResponse
from time import time

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_tracker = {}

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chat/"):
            ip = request.META.get('REMOTE_ADDR')
            now = time()
            messages = self.ip_message_tracker.get(ip, [])
            # Remove messages older than 60 seconds
            messages = [msg_time for msg_time in messages if now - msg_time < 60]
            if len(messages) >= 5:
                return JsonResponse({"error": "Rate limit exceeded. Max 5 messages per minute."}, status=429)
            messages.append(now)
            self.ip_message_tracker[ip] = messages
        return self.get_response(request)
