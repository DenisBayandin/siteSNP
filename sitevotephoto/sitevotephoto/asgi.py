import os

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

import WebSocket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitevotephoto.settings')
application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            WebSocket.routing.websocket_urlpatterns
        )
    )
})
