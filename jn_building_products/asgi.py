"""
ASGI config for J&N Building Products.
Uses Django Channels for WebSocket support, with Redis channel layer.
"""

import os

# Set the Django settings module FIRST – before any Django import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jn_building_products.settings_production')

# Initialize Django ASGI application (this runs django.setup())
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

# Now it's safe to import Channels components (they use Django models/settings)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from core.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})
