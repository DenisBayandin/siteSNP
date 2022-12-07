from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from easy_thumbnails.fields import ThumbnailerImageField


class User(AbstractUser):
    fio = models.CharField(max_length=100, verbose_name="ФИО", null=True)
    photoUser = ThumbnailerImageField(verbose_name="Фото", blank=True, upload_to='photos/%Y/%m/%d', resize_source=dict(size=(300,300), quality=80, crop=True))
    dateCreateUser = models.DateField(auto_now_add=True, verbose_name="Дата создания профиля", null=True)
    dateUpdateUser = models.DateTimeField(auto_now=True, verbose_name="Дата и время когда user был обновлен")
    usualUserOrModer = models.BooleanField(default=False, verbose_name='Модератор?')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Юзер"
        verbose_name_plural = "Юзеры"
        # ordering = ['-dateCreateUser']

class Photo(models.Model):
    photoID = models.BigAutoField(primary_key=True)
    namePhoto = models.CharField(max_length=150, verbose_name='Название фотографии ')
    сontentPhoto = models.TextField(blank=True, verbose_name='Описание к фотографии')
    dateCreatePhoto = models.DateField(auto_now_add=True, verbose_name="Дата добавления фотографии")
    dateUpdatePhoto = models.DateTimeField(auto_now=True, verbose_name="Дата и время когда фотография была обновлена")
    InfoPublishedPhoto = models.BooleanField(default=False, verbose_name='Опубликовать?')
    DeletePhoto = models.BooleanField(default=False, verbose_name='Отправлено на удаление?')
    ModificationPhoto = models.BooleanField(default=False, verbose_name='Изменили фотографию?')
    newPhoto = models.ImageField(verbose_name='Фотография', blank=False, upload_to='photos_main/%Y/%m/%d')
    oldPhoto = models.ImageField(verbose_name='Старая фотография', blank=True, upload_to='photos_old/%Y/%m/%d')
    photo_145x165 = ThumbnailerImageField(verbose_name="Фото размером 145x165", blank=True, upload_to='photos_145x165/%Y/%m/%d', resize_source=dict(size=(145, 165), quality=80, crop=True))
    photo_510x510 = ThumbnailerImageField(verbose_name="Фото размером 510x510", blank=True, upload_to='photos_510x510/%Y/%m/%d', resize_source=dict(size=(510, 510), quality=80, crop=True))
    photo_1680x1680 = ThumbnailerImageField(verbose_name="Фото размером 1680х1680", blank=True, upload_to='photos_1680x1680/%Y/%m/%d', resize_source=dict(size=(1680, 1680), quality=80, crop=True))
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.photoID
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

