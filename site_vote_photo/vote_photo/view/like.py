import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..services.like import AddLikeService

from ..models import *


def add_like(request):
    # TODO Функция создания и удаления лайка.
    """
    Сперва получаем ID фотографии
    Затем проверяем, поставил ли пользователь лайк на нашу фотографию
    Если да, то получаем лайк, удаляем его и уменьшем кол-во лайков на 1,
     отправляем status 200
    Если нет, получаем фотографию,
     создаём лайк и передаём пользователя и фотографию,
    а после этого увеличиваем кол-во лайков на 1 и отправляем status 200
    """
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        data = json.load(request)
        if is_ajax:
            if request.method == "POST":
                if AddLikeService.execute(
                    {
                        "user": request.user,
                        "photo": get_object_or_404(Photo, id=data.get("photoID")),
                    }
                ):
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=201)
        else:
            return HttpResponse("Ошибка.", status=400, reason="Invalid request")
    else:
        return HttpResponse(status=202)
