from vote_photo.model.photo.photo import Photo
from vote_photo.model.user.user import User

from django.db import models


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Поставил лайк"
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        verbose_name="Фотография, которая содержит лайк",
    )
    date_create = models.DateField(
        auto_now_add=True, verbose_name="Дата добавления лайка"
    )
    date_update = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время когда клайк был обновлён"
    )

    def __str__(self):
        return f"{self.user} - лайкнул фотографию {self.photo.name}"

    class Meta:
        db_table = "likes"
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
