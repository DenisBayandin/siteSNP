from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# User = get_user_model()


class User(AbstractUser):
    fio = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    photoUser = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True)
    dateCreateUser = models.DateField(auto_now_add=True, verbose_name="Дата создания профиля")
    dateUpdateUser = models.DateTimeField(auto_now=True, verbose_name="Дата и время когда user был обновлен")
    usualUserOrModer = models.BooleanField(default=False, verbose_name='Модератор?')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Юзер"
        verbose_name_plural = "Юзеры"
        # ordering = ['-dateCreateUser']
