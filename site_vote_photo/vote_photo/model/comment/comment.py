from vote_photo.model.photo.photo import Photo
from vote_photo.model.user.user import User

from django.urls import reverse
from django.db import models


class Comment(models.Model):
    content = models.TextField(blank=False)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse("show_comment", kwargs={"commentID": self.pk})

    class Meta:
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.content
