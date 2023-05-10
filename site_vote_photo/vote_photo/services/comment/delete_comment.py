from service_objects.services import Service
from service_objects.fields import ModelField
from django.core.exceptions import ValidationError

from vote_photo.models import *


class DeleteCommentService(Service):
    comment = ModelField(Comment)
    user = ModelField(User)

    def process(self):
        self.check_children_comment(
            self.cleaned_data["comment"], self.cleaned_data["user"]
        )

    def check_children_comment(self, comment, user):
        for comment_children in Comment.objects.filter(parent=comment.id):
            if comment_children.parent.id == comment.id:
                raise ValidationError("Невозможно удалить данный комментарий.")
        self.check_delete_comment(user, comment)

    def check_delete_comment(self, user, comment):
        if user == comment.user:
            comment.delete()
