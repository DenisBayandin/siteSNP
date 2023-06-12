from service_objects.services import Service
from service_objects.fields import ModelField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime, timedelta

from vote_photo.models import *
from ..telegram.send_message import send_message_is_telegram


channel_layer = get_channel_layer()


class ServiceDeletePhoto(Service):
    photo = ModelField(Photo)
    user = ModelField(User)

    def process(self):
        self.change_data_photo_and_state_photo(self.cleaned_data["photo"])
        self.check_to_whom_send_notification_and_send_notification()

    def check_to_whom_send_notification_and_send_notification(self):
        check_send_notification = []
        for comment in Comment.objects.filter(photo_id=self.cleaned_data["photo"].id):
            get_user = User.objects.get(id=comment.user_id)
            if get_user.id in check_send_notification:
                continue
            else:
                if self.cleaned_data["user"] == get_user:
                    continue
                try:
                    user, message = self.send_notification(
                        self.cleaned_data["photo"],
                        get_user,
                        check_send_notification,
                        self.cleaned_data["user"],
                    )
                    self.cleaned_data["photo"].save()
                    self.send_message_telegram(user, message)
                except TypeError:
                    continue

    # TODO Нотификация при удаление фотографии.
    def send_notification(self, photo, user, check_notification, req_user):
        check_notification.append(user.id)
        notification_comment_on_the_photo_delete = Notification.objects.create(
            sender=req_user,
            recipient=user,
            message=(
                f"Ваш/Ваши комментарий/комментарии "
                f"к фотографии '{photo.name}' "
                f"скоро будет/будут удалён/удалены, так как "
                f"фотография отправлена на удаление."
            ),
        )
        async_to_sync(channel_layer.group_send)(
            user.group_name,
            {
                "type": "send_new_data",
                "message": notification_comment_on_the_photo_delete.message,
            },
        )
        return user, notification_comment_on_the_photo_delete.message

    def send_message_telegram(self, user, message):
        if user.status == "Offline":
            send_message_is_telegram(user, message)

    def change_data_photo_and_state_photo(self, photo):
        photo.date_delete = datetime.now() + timedelta(minutes=15)
        photo.go_state_photo_delete()
