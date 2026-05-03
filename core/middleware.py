# core/middleware.py
from .models import Visitor


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip admin and static requests to avoid noise
        if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            referrer = request.META.get('HTTP_REFERER', '')

            Visitor.objects.create(
                path=request.path,
                ip_address=ip,
                user_agent=user_agent,
                device_type=Visitor.get_device_type(user_agent),
                browser=Visitor.get_browser(user_agent),
                referrer=referrer,
            )

        response = self.get_response(request)
        return response