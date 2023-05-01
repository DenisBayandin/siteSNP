from service_objects.services import Service
from django.forms import ModelChoiceField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms

from vote_photo.models import *


channel_layer = get_channel_layer()


class ServiceSendNotificationAllUser(Service):
    message_notification = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        self.send_notification(
            self.cleaned_data["message_notification"], self.cleaned_data["user"]
        )

    def send_notification(self, message_notification, user):
        notification = Notification.objects.create(
            sender=user,
            message=f"Админ/модератор отправил сообщение: {message_notification}",
        )
        async_to_sync(channel_layer.group_send)(
            "notification_admin",
            {"type": "send_new_data", "message": notification.message},
        )
