from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from service_objects.services import Service
from django.forms import ModelChoiceField
from asgiref.sync import async_to_sync


from ..mymodels.model_comment import Comment
from ..mymodels.model_photo import Photo
from ..mymodels.model_notification import Notification
from ..mymodels.model_user import User


channel_layer = get_channel_layer()


class DeleteCommentService(Service):
    comment = ModelChoiceField(queryset=Comment.objects.all())
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        comment = self.cleaned_data["comment"]
        self.check_children_comment(comment, user)

    def check_children_comment(self, comment, user):
        for comment_children in Comment.objects.filter(parent=comment.id):
            if comment_children.parent.id == comment.id:
                raise ValidationError("Невозможно удалить данный комментарий.")
        self.check_delete_comment(user, comment)

    def check_delete_comment(self, user, comment):
        if user == comment.user:
            comment.delete()


class SendNotificationCommentService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        photo = self.cleaned_data["photo"]
        user = self.cleaned_data["user"]
        self.send_notification(photo, user)

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
