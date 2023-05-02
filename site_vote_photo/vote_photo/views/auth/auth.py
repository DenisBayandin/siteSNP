from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from rest_framework.authtoken.models import Token
from rest_framework import status

from ...myexception.not_valided_password import UpdatePasswordExciption
from vote_photo.forms import (
    RegisterUsersForm,
    LoginUsersForm,
    AddPhotoForm,
    UpdatePasswordForm,
)
from vote_photo.views.update.update_token_by_vk import rename_lifetime_token_vk
from vote_photo.services.photo.get_photo_from_vk import (
    ProfileGetPhotoFromVkService,
)
from vote_photo.services.updatedata.update_password import ServiceUpdatePassword
from vote_photo.services.photo.save_photo_with_new_size import NewSizePhotoService


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
    token = Token.objects.get_or_create(user=request.user)
    user = request.user
    if user.photo_by_user.name == "":
        ProfileGetPhotoFromVkService.execute({"user": request.user})
    if request.method == "POST":
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            NewSizePhotoService.execute({"photo": obj})
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
            "token": token[0].key,
        },
    )


def update_password(request):
    if request.method == "POST":
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            try:
                ServiceUpdatePassword.execute(
                    {
                        "password": request.POST["password"],
                        "new_password": request.POST["new_password"],
                        "new_password2": request.POST["new_password2"],
                        "user": request.user,
                    }
                )
            except ValueError:
                return HttpResponse(
                    "Новые пароли не сходятся.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except ValidationError:
                return HttpResponse(
                    "Ввели не верный основной пароль.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except UpdatePasswordExciption as error:
                return HttpResponse(f"{error}", status=status.HTTP_400_BAD_REQUEST)
            return redirect("login")
        else:
            return HttpResponse(
                "form.is_valid() == False", status=status.HTTP_400_BAD_REQUEST
            )


def logout_view(request):
    # TODO Функция выхода из сессии.
    logout(request)
    return redirect("main")
