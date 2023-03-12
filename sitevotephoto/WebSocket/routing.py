from django.urls import path

from WebSocket.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/test_ws/<int:user_pk>/', NotificationConsumer.as_asgi()),
]
