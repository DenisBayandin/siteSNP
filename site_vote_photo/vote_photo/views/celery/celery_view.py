from celery import shared_task
from django.shortcuts import get_object_or_404, redirect

from vote_photo.services.photo.celery_delete_photo import ServiceCeleryDeletePhoto
from vote_photo.services.photo.delete_photo import ServiceDeletePhoto
from vote_photo.models import *


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
    return ServiceCeleryDeletePhoto.execute({"name": "what it's you input?"})


def delete_photo(request, photoID):
    # TODO Функция для удаления фотографий.
    """
    Функция получает фотографию, после чего заносит в БД данные о времени,
     когда её нужно удалить
    меняет state на delete.
    Отпрвляем увдомление, о том, что комментарий будет удалён,
     так как фотография отправлена на удаление.
    """
    ServiceDeletePhoto.execute(
        {"photo": get_object_or_404(Photo, id=photoID), "user": request.user}
    )
    return redirect("all_photo")
