"""
ASGI config for beylbackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

#DJANGO CHANNELS CONFIGURATION
from channels.routing import ProtocolTypeRouter, URLRouter
from channels import auth
import chat.routing

from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application  = ProtocolTypeRouter({
    'http' : get_asgi_application(),
})

