import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from vote_photo.models import User
from vote_photo.services.updatedata.update_token import UpdateTokenService
from vote_photo.services.updatedata.update_profile import ServiceRenameProfile


def update_token(request):
    # TODO Функция генерирования нового токена.
    """
    Получаем TOKEN по текущему пользователю.
    После чего удаляем его и создаём новый, передавая текущего юзера
    И отправляем статус, токен в асинхронный запрос.
    """
    token = UpdateTokenService.execute(
        {"token": get_object_or_404(Token, user=request.user.id), "user": request.user}
    )
    data = {"status": 200, "token": str(token)}
    return JsonResponse(data)


def update_data_profile(request):
    # TODO Функция для переименования данных в профиле.
    """
    data - данные, которые пришли с javascript при
     работе асинхронного запроса
    new_... - переменные, в которых хранятся данные
     нового имени, фамилии и т.п.
    Функция получает новые данные с асинхронного запроса,
    после чего получаем текущего пользователя  и
     перезаписываем его поля новыми данными
    Если всё прошло хорошо, то отправляем статус 200
    иначе статус 400.
    """

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    data = json.load(request)
    if is_ajax:
        if request.method == "POST":
            ServiceRenameProfile.execute(
                {
                    "username": data.get("new_username"),
                    "first_name": data.get("new_name"),
                    "last_name": data.get("new_family"),
                    "patronymic": data.get("new_patronymic"),
                    "email": data.get("new_email"),
                    "user": User.objects.get(id=request.user.id),
                }
            )
            return HttpResponse(status=200)
    else:
        return HttpResponse("Ошибка.", status=400, reason="Invalid request")
