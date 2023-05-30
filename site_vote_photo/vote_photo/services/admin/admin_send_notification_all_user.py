from service_objects.fields import ModelField
from service_objects.services import Service
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms
from ...utils.services.custom_service import ServiceWithResult
from rest_framework import status

from vote_photo.models import *


channel_layer = get_channel_layer()


# class ServiceSendNotificationAllUser321(Service):
#     message_notification = forms.CharField()
#     user = ModelField(User)
#
#     def process(self):
#         self.send_notification(
#             self.cleaned_data["message_notification"], self.cleaned_data["user"]
#         )
#
#     def send_notification(self, message_notification, user):
#         notification = Notification.objects.create(
#             sender=user,
#             message=f"Админ/модератор отправил сообщение: {message_notification}",
#         )
#         async_to_sync(channel_layer.group_send)(
#             "notification_admin",
#             {"type": "send_new_data", "message": notification.message},
#         )


class ServiceSendNotificationAllUser(ServiceWithResult):
    message_notification = forms.CharField()
    user = ModelField(User)

    custom_validations = ["check_rights_user"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.send_notification(
                self.cleaned_data["message_notification"], self.cleaned_data["user"]
            )
        return self

    def send_notification(self, message_notification, user):
        notification = Notification.objects.create(
            sender=user,
            message=f"Админ/модератор отправил сообщение: {message_notification}",
        )
        async_to_sync(channel_layer.group_send)(
            "notification_admin",
            {"type": "send_new_data", "message": notification.message},
        )

    def check_rights_user(self):
        if not (
            self.cleaned_data["user"].is_superuser
            and self.cleaned_data["user"].is_staff
        ):
            self.add_error(
                "id",
                f"The user does not have the right to perform this function.",
            )
            self.response_status = status.HTTP_404_NOT_FOUND
