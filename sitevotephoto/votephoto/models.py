import io

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from PIL import Image as Img
from io import BytesIO
import os.path
from django.core.files.uploadedfile import InMemoryUploadedFile


class User(AbstractUser):
    patronymic = models.CharField(max_length=50,
                                  verbose_name="Отчество",
                                  null=True
                                  )
    photo_by_user = ThumbnailerImageField(verbose_name="Photo by user",
                                          blank=True,
                                          upload_to='photos/%Y/%m/%d',
                                          resize_source=dict(size=(300, 300),
                                                             quality=80,
                                                             crop=True
                                                             )
                                          )
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    moderator = models.BooleanField(default=False,
                                    verbose_name='Is he a moderator?'
                                    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Юзер"
        verbose_name_plural = "Юзеры"
        # ordering = ['-dateCreateUser']


class Photo(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    info_published = models.BooleanField(default=False, verbose_name='To publish?')
    delete_photo = models.BooleanField(default=False, verbose_name='Delete photo?')
    modification = models.BooleanField(default=False)
    new_photo = models.ImageField(blank=False, upload_to='new_photos/%Y/%m/%d')
    old_photo = models.ImageField(blank=True, upload_to='old_photos/%Y/%m/%d')
    photo_145x165 = models.ImageField(blank=True, upload_to='photos_145x165/%Y/%m/%d')
    photo_510x510 = models.ImageField(blank=True, upload_to='photos_510x510/%Y/%m/%d')
    count_like = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('show_photo', kwargs={'photoID': self.pk})

    def __str__(self):
        return f'Name photo: {self.name}'

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
        ordering = ('-date_create', )

    def save(self, *args, **kwargs):
        image_bytes = BytesIO(self.old_photo.read())
        image = Img.open(image_bytes)
        image.thumbnail((510, 510), Img.ANTIALIAS)
        output = BytesIO()
        image.save(output, format='JPEG', quality=90)
        output.seek(0)
        self.photo_510x510 = InMemoryUploadedFile(output, 'ImageField', self.old_photo.name, 'image/jpeg',
                                                  output.__sizeof__(), None)
        super(Photo, self).save(*args, **kwargs)

        image.thumbnail((145, 165), Img.ANTIALIAS)
        output = BytesIO()
        image.save(output, format='JPEG', quality=90)
        output.seek(0)
        self.photo_145x165 = InMemoryUploadedFile(output, 'ImageField', self.old_photo.name, 'image/jpeg',
                                                  output.__sizeof__(), None)
        super(Photo, self).save(*args, **kwargs)



class Comment(models.Model):
    content = models.TextField(blank=False)
    dateCreate = models.DateField(auto_now_add=True)
    dateUpdate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    Parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('show_comment', kwargs={'commentID': self.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="Поставил лайк"
                             )
    photo = models.ForeignKey(Photo,
                              on_delete=models.CASCADE,
                              verbose_name="Пост, который содержит лайк"
                              )
    dateCreate = models.DateField(auto_now_add=True,
                                  verbose_name="Дата добавления лайка"
                                  )
    dateUpdate = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата и время когда клайк был обновлён"
                                      )

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user} - лайкнул фотографию {self.photo.name}"
