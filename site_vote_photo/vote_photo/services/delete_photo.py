from service_objects.services import Service
from django.forms import ModelChoiceField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime, timedelta

from ..models import *


channel_layer = get_channel_layer()


class ServiceDeletePhoto(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    req_user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        self.change_data_photo_and_state_photo(self.cleaned_data["photo"])
        check_send_notification = []
        for comment in Comment.objects.filter(photo_id=self.cleaned_data["photo"].id):
            get_user = User.objects.get(id=comment.user_id)
            if get_user.id in check_send_notification:
                continue
            else:
                if self.cleaned_data["req_user"] == get_user:
                    continue
                try:
                    self.send_notification(
                        self.cleaned_data["photo"],
                        get_user,
                        check_send_notification,
                        self.cleaned_data["req_user"],
                    )
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

    def change_data_photo_and_state_photo(self, photo):
        photo.date_delete = datetime.now() + timedelta(minutes=15)
        photo.go_state_photo_delete()
        photo.save()
