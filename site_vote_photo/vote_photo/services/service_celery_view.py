from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from service_objects.services import Service
from django.forms import ModelChoiceField
from datetime import datetime, timedelta
from django.utils import timezone


from ..mymodels.model_photo import Photo
from ..mymodels.model_comment import Comment
from ..mymodels.model_user import User
from ..mymodels.model_notification import Notification


channel_layer = get_channel_layer()


class ServiceDeletePhoto(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    req_user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        req_user = self.cleaned_data["req_user"]
        photo = self.cleaned_data["photo"]
        self.change_data_photo_and_state_photo(photo)
        check_send_notification = []
        for comment in Comment.objects.filter(photo_id=photo.id):
            get_user = User.objects.get(id=comment.user_id)
            if get_user.id in check_send_notification:
                continue
            else:
                if req_user == get_user:
                    continue
                try:
                    self.send_notification(
                        photo, get_user, check_send_notification, req_user
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


class ServiceCeleryDeletePhoto(Service):
    def process(self):
        photo_delete_all = Photo.objects.filter(state="Delete")
        count_photo_delete = Photo.objects.filter(state="Delete").count()
        self.check_the_time_and_delete(photo_delete_all)
        return self.what_to_return_to_the_main_function(count_photo_delete)

    def check_the_time_and_delete(self, queryset_photo):
        for one_photo_delete in queryset_photo:
            if timezone.now() >= one_photo_delete.date_delete:
                one_photo_delete.delete()

    def what_to_return_to_the_main_function(self, count_photo):
        if count_photo >= 1:
            return "There are photos to delete."
        else:
            return "No photos to delete."
