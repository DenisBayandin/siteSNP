from django.contrib.auth.models import AbstractUser
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from PIL import Image as Img
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



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
    photo_145x165 = models.ImageField(verbose_name='Фотография размером 145x165', blank=True, upload_to='photos_145x165/%Y/%m/%d')
    photo_510x510 = models.ImageField(verbose_name='Фотография размером 510x510', blank=True, upload_to='photos_510x510/%Y/%m/%d')
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.photoID
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def save(self, *args, **kwargs):
        image = Img.open(BytesIO(self.oldPhoto.read()))
        image.thumbnail((145, 165), Img.ANTIALIAS)
        output = BytesIO()
        image.save(output, format='JPEG', quality=75)
        output.seek(0)
        self.photo_145x165 = InMemoryUploadedFile(output, 'ImageField', self.oldPhoto.name, 'image/jpeg',
                                                  output.__sizeof__(), None)
        super(Photo, self).save(*args, **kwargs)

        image = Img.open(BytesIO(self.oldPhoto.read()))
        image.thumbnail((510, 510), Img.ANTIALIAS)
        output = BytesIO()
        image.save(output, format='JPEG', quality=75)
        output.seek(0)
        self.photo_510x510 = InMemoryUploadedFile(output, 'ImageField', self.oldPhoto.name, 'image/jpeg',
                                                  output.__sizeof__(), None)
        super(Photo, self).save(*args, **kwargs)



