from .models import Visitor

EXCLUDED_PATHS = ('/admin/', '/static/', '/media/', '/favicon.ico',
                  '/log-whatsapp-click/', '/htmx/', '/admin/dashboard/')


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Only track successful GET requests to public pages
        if (request.method == 'GET'
                and response.status_code == 200
                and not any(request.path.startswith(p) for p in EXCLUDED_PATHS)
                and not request.path.startswith('/admin')):
            try:
                ua = request.META.get('HTTP_USER_AGENT', '')
                ip = (request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
                      or request.META.get('REMOTE_ADDR', '127.0.0.1'))
                Visitor.objects.create(
                    path=request.path,
                    ip_address=ip,
                    user_agent=ua,
                    device_type=Visitor.get_device_type(ua),
                    browser=Visitor.get_browser(ua),
                    referrer=request.META.get('HTTP_REFERER', ''),
                )
            except Exception:
                pass  # Never break the site for analytics
        return response
