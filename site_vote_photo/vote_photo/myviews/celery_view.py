from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from ..models import Photo, Comment, User, Notification
from ..services.service_celery_view import *

channel_layer = get_channel_layer()


@shared_task(name="celery_delete_photo")
def celery_delete_photo():
    # TODO Функция проверяющая текущую дату и дату удаления,
    #  если текущая дата >= даты удаления удаляем фотографию.
    """
    Получаем фотографии со state = Delete и их количество
    После чего для каждой такой фотографии меняем поле
     date_now на текущее время
    Далее проверяем, если текущее время больше времени,
     когда фотографию нужно удалить,
    То фотографию удаляем.
    """
    return ServiceCeleryDeletePhoto.execute()


def delete_photo(request, photoID):
    # TODO Функция для удаления фотографий.
    """
    Функция получает фотографию, после чего заносит в БД данные о времени,
     когда её нужно удалить
    меняет state на delete.
    Отпрвляем увдомление, о том, что комментарий будет удалён,
     так как фотография отправлена на удаление.
    """
    ServiceDeletePhoto.execute({"photo": get_object_or_404(Photo, id=photoID)})
    return redirect("all_photo")
