from service_objects.services import Service
from service_objects.fields import ModelField
from django.core.exceptions import ValidationError

from vote_photo.models import *


class DeleteCommentService(Service):
    comment = ModelField(Comment)
    user = ModelField(User)

    def process(self):
        if self.repay_true_if_not_children_comment(
            self.cleaned_data["comment"], self.cleaned_data["user"]
        ):
            self.delete_comment(self.cleaned_data["user"], self.cleaned_data["comment"])

    def repay_true_if_not_children_comment(self, comment, user):
        if Comment.objects.filter(parent=comment.id).first() is not None:
            raise ValidationError("Невозможно удалить данный комментарий.")
        return True

    def delete_comment(self, user, comment):
        if user == comment.user:
            comment.delete()
