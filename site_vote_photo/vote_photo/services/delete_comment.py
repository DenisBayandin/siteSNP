from service_objects.services import Service
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError

from ..models import *


class DeleteCommentService(Service):
    comment = ModelChoiceField(queryset=Comment.objects.all())
    user = ModelChoiceField(queryset=User.objects.all())

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
