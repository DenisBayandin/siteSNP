from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from ..models import Photo, Comment, User, Notification

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
    photo_delete_all = Photo.objects.filter(state="Delete")
    count_photo_delete = Photo.objects.filter(state="Delete").count()
    for one_photo_delete in photo_delete_all:
        if timezone.now() >= one_photo_delete.date_delete:
            one_photo_delete.delete()
    if count_photo_delete >= 1:
        return "There are photos to delete."
    else:
        return "No photos to delete."


def delete_photo(request, photoID):
    # TODO Функция для удаления фотографий.
    """
    Функция получает фотографию, после чего заносит в БД данные о времени,
     когда её нужно удалить
    меняет state на delete.
    Отпрвляем увдомление, о том, что комментарий будет удалён,
     так как фотография отправлена на удаление.
    """
    photo = get_object_or_404(Photo, id=photoID)
    photo.date_delete = datetime.now() + timedelta(minutes=15)
    photo.go_state_photo_delete()
    photo.save()
    check_send_notification = []
    for comment in Comment.objects.filter(photo_id=photo.id):
        get_user = User.objects.get(id=comment.user_id)
        if get_user.id in check_send_notification:
            continue
        else:
            # TODO Нотификация при удаление фотографии.
            check_send_notification.append(get_user.id)
            notification_comment_on_the_photo_delete = Notification.objects.create(
                message=(
                    f"Ваш/Ваши комментарий/комментарии "
                    f"к фотографии '{photo.name}' "
                    f"скоро будет/будут удалён/удалены, так как "
                    f"фотография отправлена на удаление."
                )
            )
            async_to_sync(channel_layer.group_send)(
                get_user.group_name,
                {
                    "type": "send_new_data",
                    "message": notification_comment_on_the_photo_delete.message,
                },
            )
    return redirect("all_photo")
