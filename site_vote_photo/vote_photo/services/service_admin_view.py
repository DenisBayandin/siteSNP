from django.shortcuts import get_object_or_404
from service_objects.services import Service
from django.forms import ModelChoiceField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from ..mymodels.model_photo import Photo
from ..mymodels.model_notification import Notification
from ..mymodels.model_user import User


channel_layer = get_channel_layer()


class ShowPhotoAdminService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        photo = self.cleaned_data["photo"]
        self.change_state(photo)
        return photo

    def change_state(self, photo):
        if photo.state == "On check":
            photo.go_state_not_verified()
            photo.go_state_on_check()
            photo.save()
        else:
            photo.go_state_on_check()
            photo.save()


class UpdateStateOnVerifiedService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        photo = self.cleaned_data["photo"]
        self.change_state(photo)
        self.send_notification(photo)

    def change_state(self, photo):
        photo.go_state_verified()
        photo.save()

    def send_notification(self, photo):
        get_user = User.objects.get(id=photo.user_id)
        notification = Notification.objects.create(
            message=f"Вашу фотографию '{photo.name}' одобрили."
        )
        async_to_sync(channel_layer.group_send)(
            get_user.group_name,
            {"type": "send_new_data", "message": notification.message},
        )


class UpdateStateOnNotVerifiedService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        photo = self.cleaned_data["photo"]
        self.change_state(photo)
        self.send_notification(photo)

    def change_state(self, photo):
        photo.go_state_not_verified()
        photo.save()

    def send_notification(self, photo):
        get_user = User.objects.get(id=photo.user_id)
        notification = Notification.objects.create(
            message=f"Вашу фотографию '{photo.name}' отклонили."
        )
        async_to_sync(channel_layer.group_send)(
            get_user.group_name,
            {"type": "send_new_data", "message": notification.message},
        )


class UpdateOldPhotoOnNewPhotoService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        photo = self.cleaned_data["photo"]
        self.change_photo(photo)
        self.change_state(photo)
        self.send_notification(photo)

    def change_state(self, photo):
        photo.go_state_verified()
        photo.save()

    def change_photo(self, photo):
        photo.old_photo = photo.new_photo
        photo.new_photo = None

    def send_notification(self, photo):
        get_user = User.objects.get(id=photo.user_id)
        notification = Notification.objects.create(
            message=f"Вам одобрили изменение данных или фотографии '{photo.name}'."
        )
        async_to_sync(channel_layer.group_send)(
            get_user.group_name,
            {"type": "send_new_data", "message": notification.message},
        )
