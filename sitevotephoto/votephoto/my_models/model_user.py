from django.contrib.auth.models import AbstractUser
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class User(AbstractUser):
    patronymic = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        null=True
    )
    photo_by_user = ThumbnailerImageField(
        verbose_name="Photo by user",
        null=True,
        blank=True,
        upload_to='photos/%Y/%m/%d',
        resize_source=dict(size=(300, 300),
                           quality=80,
                           crop=True
                           )
    )
    url_photo_by_user_from_VK = models.URLField(null=True)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    @property
    def group_name(self):
        return f"user_{self.pk}s"

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_votephoto'
        verbose_name = "Юзер"
        verbose_name_plural = "Юзеры"

