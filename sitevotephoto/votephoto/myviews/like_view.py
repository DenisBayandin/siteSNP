import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..models import Like, Photo


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
        photoID = data.get("photoID")
        if is_ajax:
            if request.method == "POST":
                if Like.objects.filter(photo=photoID, user=request.user).exists():
                    one_like_user = Like.objects.get(photo=photoID, user=request.user)
                    one_like_user.delete()
                    return HttpResponse(status=200)
                else:
                    photo = get_object_or_404(Photo, pk=photoID)
                    like = Like()
                    like.user = request.user
                    like.photo = photo
                    like.save()
                    return HttpResponse(status=201)
        else:
            return HttpResponse("Ошибка.", status=400, reason="Invalid request")
    else:
        return HttpResponse(status=202)
