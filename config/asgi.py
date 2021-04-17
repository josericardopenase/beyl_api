"""
ASGI config for beylbackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django_asgi_app = get_asgi_application()

from django.contrib.auth.models import AnonymousUser
#DJANGO CHANNELS CONFIGURATION
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns
from utils.websockets.TokenAuthMiddleware import TokenAuthMiddleware

application  = ProtocolTypeRouter({
    'http' : django_asgi_app,
    'websocket' : TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
})


