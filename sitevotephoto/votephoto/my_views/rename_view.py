import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from ..models import *


def rename_token(request):
    # TODO Функция генерирования нового токена.
    """
        Получаем TOKEN по текущему пользователю.
        После чего удаляем его и создаём новый, передавая текущего юзера
        И отправляем статус, токен в асинхронный запрос.
    """
    token = get_object_or_404(Token, user=request.user.pk)
    token.delete()
    token = Token.objects.create(user=request.user)
    data = {"status": 200, "token": str(token)}
    return JsonResponse(data)
    # try:
    #     return jsonify(data)
    # except:
    #     breakpoint()


def rename_profile(request):
    # TODO Функция для переименования данных в профиле.
    """
        data - данные, которые пришли с javascript при работе асинхронного запроса
        new_... - переменные, в которых хранятся данные нового имени, фамилии и т.п.
        Функция получает новые данные с асинхронного запроса,
        после чего получаем текущего пользователя  и перезаписываем его поля новыми данными
        Если всё прошло хорошо, то отправляем статус 200
        иначе статус 400.
    """

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    data = json.load(request)
    new_name = data.get('new_name')
    new_family = data.get('new_family')
    new_patronymic = data.get('new_patronymic')
    new_email = data.get('new_email')
    new_username = data.get('new_username')
    if is_ajax:
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.pk)
            user.username = new_username
            user.first_name = new_name
            user.last_name = new_family
            user.patronymic = new_patronymic
            user.email = new_email
            user.save()
            return HttpResponse(status=200)
    else:
        # user = vk.method("users.get", {"user_ids": 1, "fields": ["photo_max_orig"]})
        return HttpResponse("Ошибка.", status=400, reason='Invalid request')

