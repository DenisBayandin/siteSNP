from service_objects.services import Service
from service_objects.fields import ModelField
from django.core.exceptions import ValidationError
from ...utils.services.custom_service import ServiceWithResult
from rest_framework import status

from vote_photo.models import *


class DeleteCommentService(ServiceWithResult):
    comment = ModelField(Comment)
    user = ModelField(User)

    custom_validations = [
        "repay_true_if_not_children_comment",
        "validation_user_id_equals_comment_user_id"
    ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.delete_comment(self.cleaned_data["comment"])
        return self

    def delete_comment(self, comment):
        comment.delete()

    def repay_true_if_not_children_comment(self):
        if (
            Comment.objects.filter(parent=self.cleaned_data["comment"].id).first()
            is not None
        ):
            self.add_error("id", "It is not possible to delete this comment.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise ValidationError("Невозможно удалить комментарий.")

    def validation_user_id_equals_comment_user_id(self):
        if self.cleaned_data["user"].id != self.cleaned_data["comment"].user.id:
            self.add_error("id", "The user is not the owner of the comment.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise ValidationError("Невозможно удалить комментарий.")
