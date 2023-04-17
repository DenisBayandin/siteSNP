from service_objects.services import Service
from django.forms import ModelChoiceField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..models import *

channel_layer = get_channel_layer()


class UpdateStateOnNotVerifiedService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        self.change_state(self.cleaned_data["photo"])
        self.send_notification(self.cleaned_data["photo"], self.cleaned_data["user"])

    def change_state(self, photo):
        photo.go_state_not_verified()
        photo.save()

    def send_notification(self, photo, user):
        get_user = User.objects.get(id=photo.user_id)
        notification = Notification.objects.create(
            sender=user,
            recipient=get_user,
            message=f"Вашу фотографию '{photo.name}' отклонили.",
        )
        async_to_sync(channel_layer.group_send)(
            get_user.group_name,
            {"type": "send_new_data", "message": notification.message},
        )
