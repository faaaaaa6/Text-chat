"""
ASGI config for textchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE','textchat.settings')

application = ProtocolTypeRouter({ #to cheack wheather it's a http or websocket request
   'http': get_asgi_application(),
   'websocket': AuthMiddlewareStack(
     URLRouter(
       chat.routing.websocket_urlpatterns
     )
   ),

})
