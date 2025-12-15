# restrict_chat_time.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if 21 <= current_hour or current_hour < 6:
            return HttpResponseForbidden("Chat is not available between 9 PM and 6 AM.")
        return self.get_response(request)
