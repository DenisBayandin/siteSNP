from service_objects.services import Service
from service_objects.fields import ModelField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from vote_photo.models import *
from ..telegram.send_message import send_message_is_telegram

channel_layer = get_channel_layer()


class UpdateOldPhotoOnNewPhotoService(Service):
    photo = ModelField(Photo)
    user = ModelField(User)

    def process(self):
        self.change_photo_and_state(self.cleaned_data["photo"])
        user, message = self.send_notification(self.cleaned_data["photo"], self.cleaned_data["user"])
        self.cleaned_data["photo"].save()
        self.send_message_telegram(user, message)

    def change_photo_and_state(self, photo):
        photo.old_photo = photo.new_photo
        photo.new_photo = None
        photo.go_state_verified()

    def send_notification(self, photo, user):
        get_user = User.objects.get(id=photo.user_id)
        notification = Notification.objects.create(
            sender=user,
            recipient=get_user,
            message=f"Вам одобрили изменение данных или фотографии '{photo.name}'.",
        )
        async_to_sync(channel_layer.group_send)(
            get_user.group_name,
            {"type": "send_new_data", "message": notification.message},
        )
        return get_user, notification.message

    def send_message_telegram(self, user, message):
        if user.status == "Offline":
            send_message_is_telegram(user, message)
