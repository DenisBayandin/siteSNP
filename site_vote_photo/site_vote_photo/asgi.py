import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_vote_photo.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
import web_socket.routing  # type: ignore

application = ProtocolTypeRouter(
    {
        "http": AsgiHandler(),
        "websocket": AuthMiddlewareStack(
            URLRouter(web_socket.routing.websocket_urlpatterns)
        ),
    }
)
