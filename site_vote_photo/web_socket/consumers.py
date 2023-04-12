import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from vote_photo.models import User, Photo, Notification


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return AnonymousUser()


@database_sync_to_async
def get_photo(photoID):
    try:
        return Photo.objects.get(id=photoID)
    except:
        return None


@database_sync_to_async
def create_notification(sender, photo, type_websoket, recipient):
    if type_websoket == "like":
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            message=(
                f'Пользователь {sender} поставил "Мне нравится"'
                f" фотографии: {photo.name}"
                f'\nОбщее кол-во "Мне нравится" на фотографии: {photo.count_like}'
            ),
        )
    elif type_websoket == "delete_like":
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            message=(
                f'Пользователь {sender} убрал "Мне нравится"'
                f"с фотографии: {photo.name}"
                f'\nОбщее кол-во "Мне нравится"'
                f" на фотографии: {photo.count_like}"
            ),
        )
    return notification.message


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        get_pk_user_from_url = self.scope["url_route"]["kwargs"]["user_pk"]
        user_from_db = await get_user(int(get_pk_user_from_url))
        self.group_name = user_from_db.group_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add("notification_admin", self.channel_name)
        await self.accept()

    async def websocket_receive(self, event):
        # TODO для каждого случ. передавать like, comment и через switch case.
        data = json.loads(event["text"])
        user = await get_user(int(data["sender"]))
        photo = await get_photo(int(data["photoID"]))
        user_which_create_photo = await get_user(int(photo.user_id))
        if user != user_which_create_photo:
            message = await create_notification(
                user, photo, data["type_websocket"], user_which_create_photo
            )
            new_data = {"type": "send_new_data", "message": message}
            await self.channel_layer.group_send(
                user_which_create_photo.group_name, new_data
            )
        else:
            return 0

    async def send_new_data(self, event):
        new_new_data = event.get("message")
        await self.send(json.dumps({"message": new_new_data}))

    async def disconnect(self, event):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_discard("notification_admin", self.channel_name)
        await self.close()

    async def send_notification(self, event):
        breakpoint()
        await self.send(json.dumps({"type": "websocket.send", "data": event}))
