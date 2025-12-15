# role_permission.py
from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if request.path.startswith("/admin-actions/") and not (user and user.is_authenticated and user.is_staff):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
