import vk
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from ..forms import RegisterUsersForm, LoginUsersForm, AddPhotoForm, UpdatePasswordForm
from .rename_lifetime_token import rename_lifetime_token_vk

version_vk_api = "5.131"


class RegisterUser(CreateView):
    # TODO Регистрация
    form_class = RegisterUsersForm
    template_name = "vote_photo/register.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context

    def form_valid(self, form):
        user = form.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, user)
        return redirect("profile")


class LoginUser(LoginView):
    # TODO Авторизация.
    form_class = LoginUsersForm
    template_name = "vote_photo/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context


def profile(request):
    # TODO Функция профиля, показывает все данные одного пользователя,
    #  получение TOKEN-а и добавление фотографии.
    """
    Сперва проверяем, если ли Token у текущего пользователя,
     если нет, то создаём новый
    передавая текушего пользователя
    Затем проверяем, есть ли фотография у нашего профиля,
     то бишь photo_by_user:
    (if user.photo_by_user is None:)
    Если фотографии нет, то мы проверям, можем ли мы ещё
     использовать access_token предоставленный VK
    Если время использования токена вышло, то мы logout
     и просим пользователя войти снова,
    чтобы создать новый access_token.
    Если же мы ещё можем использовать access_token,
     то мы его получаем.
    Затем получаем получаем фотографию аватарки
     в вк и записываем её url
    в url_photo_by_user_from_VK.
    """
    if rename_lifetime_token_vk(request, request.user):
        return redirect("login")
    try:
        token = Token.objects.get(user=request.user.id)
    except ObjectDoesNotExist:
        token = Token.objects.create(user=request.user)
    user = request.user
    if user.photo_by_user.name == "":
        social = user.social_auth.get(provider="vk-oauth2")
        api = vk.API(access_token=social.extra_data["access_token"], v=version_vk_api)
        json_vk = api.users.get(fields="photo_200")
        user.url_photo_by_user_from_VK = json_vk[0]["photo_200"]
        user.save()
    if request.method == "POST":
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("main")
    else:
        form = AddPhotoForm
        form_update_password = UpdatePasswordForm
    return render(
        request,
        "vote_photo/profile.html",
        {
            "form": form,
            "form_update_password": form_update_password,
            "title": "Личный кабинет",
            "token": token,
        },
    )


def update_password(request):
    if request.method == "POST":
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            if check_password(form.cleaned_data["password"], request.user.password):
                if (
                    form.cleaned_data["new_password"]
                    != form.cleaned_data["new_password2"]
                ):
                    try:
                        raise ValueError("Новые пароли не сходятся.")
                    except ValueError:
                        return HttpResponse(
                            "Новые пароли не сходятся.",
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    request.user.set_password(form.cleaned_data["new_password"])
                    request.user.save()
                    return redirect("login")
            else:
                try:
                    raise ValueError("Ввели не верный основной пароль.")
                except ValueError:
                    return HttpResponse(
                        "Ввели не верный основной пароль.",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            return HttpResponse(
                "form.is_valid() == False", status=status.HTTP_400_BAD_REQUEST
            )


def logout_view(request):
    # TODO Функция выхода из сессии.
    logout(request)
    return redirect("main")
