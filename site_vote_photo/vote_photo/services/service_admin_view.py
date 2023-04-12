from django.http import Http404
from django.shortcuts import get_object_or_404
from service_objects.services import Service
from django.forms import ModelChoiceField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms


from ..mymodels.model_photo import Photo
from ..mymodels.model_notification import Notification
from ..mymodels.model_user import User


channel_layer = get_channel_layer()


def checking_the_role_user(user):
    if not (user.is_staff and user.is_superuser):
        raise Http404(
            f"{user.username} не является админом!" f" Зайдите на другой аккаунт."
        )


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
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        photo = self.cleaned_data["photo"]
        self.change_state(photo)
        self.send_notification(photo, user)

    def change_state(self, photo):
        photo.go_state_verified()
        photo.save()

    def send_notification(self, photo, user):
        get_user = User.objects.get(id=photo.user_id)
        notification = Notification.objects.create(
            sender=user,
            recipient=get_user,
            message=f"Вашу фотографию '{photo.name}' одобрили.",
        )
        async_to_sync(channel_layer.group_send)(
            get_user.group_name,
            {"type": "send_new_data", "message": notification.message},
        )


class UpdateStateOnNotVerifiedService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        photo = self.cleaned_data["photo"]
        self.change_state(photo)
        self.send_notification(photo, user)

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


class UpdateOldPhotoOnNewPhotoService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    user = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        photo = self.cleaned_data["photo"]
        self.change_photo(photo)
        self.change_state(photo)
        self.send_notification(photo, user)

    def change_state(self, photo):
        photo.go_state_verified()
        photo.save()

    def change_photo(self, photo):
        photo.old_photo = photo.new_photo
        photo.new_photo = None

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


class ServiceSendNotificationAllUser(Service):
    message_notification = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        message_notification = self.cleaned_data["message_notification"]
        user = self.cleaned_data["user"]
        self.send_notification(message_notification, user)

    def send_notification(self, message_notification, user):
        notification = Notification.objects.create(
            sender=user,
            message=f"Админ/модератор отправил сообщение: {message_notification}",
        )
        async_to_sync(channel_layer.group_send)(
            "notification_admin",
            {"type": "send_new_data", "message": notification.message},
        )
