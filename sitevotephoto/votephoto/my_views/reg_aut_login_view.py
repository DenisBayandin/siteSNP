from datetime import timedelta

import vk
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import CreateView
from rest_framework.authtoken.models import Token

from ..forms import *

version_vk_api = '5.131'


class RegisterUser(CreateView):
    # TODO Регистрация
    form_class = RegisterUsersForm
    template_name = 'votephoto/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(LoginView):
    # TODO Авторизация.
    form_class = LoginUsersForm
    template_name = 'votephoto/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


def profile(request):
    # TODO Функция профиля, показывает все данные одного пользователя, получение TOKEN-а и добавление фотографии.
    """
        Сперва проверяем, если ли Token у текущего пользователя, если нет, то создаём новый
        передавая текушего пользователя
        Затем проверяем, есть ли фотография у нашего профиля, то бишь photo_by_user:
        (if user.photo_by_user is None:)
        Если фотографии нет, то мы проверям, можем ли мы ещё использовать access_token предоставленный VK
        Если время использования токена вышло, то мы logout и просим пользователя войти снова,
        чтобы создать новый access_token.
        Если же мы ещё можем использовать access_token, то мы его получаем.
        Затем получаем получаем фотографию аватарки в вк и записываем её url
        в url_photo_by_user_from_VK.
    """
    try:
        token = Token.objects.get(user=request.user.pk)
    except:
        token = Token.objects.create(user=request.user)
        token.save()
    user = request.user
    try:
        photo_user = user.photo_by_user.url
    except:
        social = user.social_auth.get(provider='vk-oauth2')
        time_life_token = social.extra_data['expires']
        time_create_token = social.created
        if time_create_token + timedelta(seconds=time_life_token) < timezone.now():
            social.created = social.modified
            social.save()
            logout(request)
            return redirect('login')
        token = social.extra_data['access_token']
        api = vk.API(access_token=token, v=version_vk_api)
        json_vk = api.users.get(fields='photo_200')
        user.url_photo_by_user_from_VK = json_vk[0]['photo_200']
        user.save()
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('main')
    else:
        form = AddPhotoForm
    return render(request, 'votephoto/profile.html', {
        'form': form,
        'title': 'Личный кабинет',
        'token': token
    })


def logout_view(request):
    # TODO Функция выхода из сессии.
    logout(request)
    return redirect('main')
