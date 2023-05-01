from django.urls import path

from web_socket.consumers import NotificationConsumer  # type: ignore

websocket_urlpatterns = [
    path("ws/test_ws/<int:user_pk>/", NotificationConsumer.as_asgi()),
]
