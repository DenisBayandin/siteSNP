from channels.layers import get_channel_layer
from service_objects.services import Service
from service_objects.fields import ModelField
from asgiref.sync import async_to_sync

from vote_photo.models import *


channel_layer = get_channel_layer()


class SendNotificationCommentService(Service):
    photo = ModelField(Photo)
    user = ModelField(User)

    def process(self):
        self.send_notification(self.cleaned_data["photo"], self.cleaned_data["user"])

    def send_notification(self, photo, user):
        get_user_create_photo = User.objects.get(id=photo.user_id)
        if user == get_user_create_photo:
            return 0
        notification = Notification.objects.create(
            recipient=get_user_create_photo,
            sender=user,
            message=(
                f"Пользователь {user.username} оставил "
                f"комментарий под фотографией: {photo.name}"
                f"\nОбщее кол-во комментариев на фотографии: {photo.count_comment}"
            ),
        )
        async_to_sync(channel_layer.group_send)(
            get_user_create_photo.group_name,
            {"type": "send_new_data", "message": notification.message},
        )
