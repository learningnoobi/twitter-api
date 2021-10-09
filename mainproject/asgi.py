from tweets.consumers import MyConsumer
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import os
import django
from chat.consumers import ChatConsumer
from .channelsmiddleware import JwtAuthMiddlewareStack


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainproject.settings")
django.setup()


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "https": get_asgi_application(),

    # WebSocket chat handler
    "websocket": JwtAuthMiddlewareStack(
        URLRouter([
             path('ws/chat/<str:username>/',ChatConsumer.as_asgi()),
            path('ws/home/', MyConsumer.as_asgi()),
           
        ])
    ),
})
