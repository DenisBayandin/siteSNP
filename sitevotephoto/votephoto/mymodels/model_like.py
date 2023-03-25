from .model_photo import User, Photo

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
    dateCreate = models.DateField(
        auto_now_add=True, verbose_name="Дата добавления лайка"
    )
    dateUpdate = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время когда клайк был обновлён"
    )

    def __str__(self):
        return f"{self.user} - лайкнул фотографию {self.photo.name}"

    class Meta:
        db_table = "like_votephoto"
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"