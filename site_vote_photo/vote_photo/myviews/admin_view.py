from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView

from ..services.service_admin_view import *

channel_layer = get_channel_layer()


class ViewPhotoNotVerified(ListView):
    # TODO Отображение фотографий со статусом
    #  state=Not verified и state=On check (админка)
    """
    Объединяем фотографии с state=On check и state=Not verified
     с той целью,
    чтобы в случае чего, мы могли снова зайти на фотографию и
     посмотреть можем ли мы её одобрить.
    Ведь если мы захотим увидеть фотографии, которые требует
     проверки то мы увидим фотографии только с
    state=Not verified и в случае обновления страницы при проверке
     фотографии у нас будет вылетать ошибка.
    """
    template_name = "vote_photo/viewPhotoNotVerified.html"
    context_object_name = "photo"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Проверка фотографий"
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            set_gueryset = set(Photo.objects.filter(state="Not verified"))
            set_photo_search_to_user = set(Photo.objects.filter(state="On check"))
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
            return super().get_queryset()
        else:
            raise Http404(
                f"{self.request.user.username} не является админом!"
                f" Зайдите на другой аккаунт!"
            )


class ViewPhotoUpdate(ListView):
    # TODO Отображение фотографий с state=Update (админка)
    template_name = "vote_photo/viewPhotoUpdate.html"
    context_object_name = "photo"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Проверка фотографий"
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            self.queryset = Photo.objects.filter(state="Update")
            return super().get_queryset()
        else:
            raise Http404(
                f"{self.request.user.username} не является админом!"
                f" Зайдите на другой аккаунт!"
            )


class ViewPhotoDelete(ListView):
    # TODO Отображение фотографий с state=Delete (админка)
    template_name = "vote_photo/viewPhotoNotVerified.html"
    context_object_name = "photo"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Проверка фотографий"
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            self.queryset = Photo.objects.filter(state="Delete")
            return super().get_queryset()
        else:
            raise Http404(
                f"{self.request.user.username} не является админом!"
                f" Зайдите на другой аккаунт!"
            )


def show_photo_admin(request, photoID):
    # TODO Функция проверки фотографии (админка)
    """
    Если пользователь имеет права админа,
     то провряем на наличие у фотографии state='On check'
    и отображаем фотографию
    """
    if request.user.is_staff and request.user.is_superuser:
        photo = ShowPhotoAdminService.execute(
            {"photo": get_object_or_404(Photo, id=photoID)}
        )
        return render(
            request,
            "vote_photo/showPhotoAdmin.html",
            {"title": "Проверка фотографии", "photo": photo},
        )
    else:
        return Http404(
            f"{request.user.username} не является админом!"
            f" Зайдите на другой аккаунт!"
        )


def show_photo_admin_update(request, photoID):
    # TODO Функция отвечающая за проверку обновления (админка)
    """
    Проверяем если пользователь имеет права админа,
     то показыаем ему фотографию.
    Иначе ошибка (Http404).
    """
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, id=photoID)
        return render(
            request,
            "vote_photo/showPhotoAdminUpdate.html",
            {"title": "Проверка фотографии", "photo": photo},
        )
    else:
        return Http404(
            f"{request.user.username} не является админом!"
            f" Зайдите на другой аккаунт!"
        )


def update_state_verified(request, photoID):
    # TODO Функция меняющая state на Verified (админка)
    """
    Получаем фотографию.
    Меняем состояние фотографии на Verified.
    Создаём и отправляем увдомление создателю фотографии,
     что его фотография прошла проверку.
    """
    if request.method == "POST":
        UpdateStateOnVerifiedService.execute(
            {"photo": get_object_or_404(Photo, id=photoID)}
        )
        return redirect("photoNotVerified")


def update_state_not_verified(request, photoID):
    # TODO Функция меняющая state на Not verified (админка)
    """
    Получаем фотографию.
    Меняем состояние фотографии на Not verified.
    Создаём и отправляем увдомление создателю фотографии,
     что его фотография не прошла проверку.
    """
    if request.method == "POST":
        UpdateStateOnNotVerifiedService.execute(
            {"photo": get_object_or_404(Photo, id=photoID)}
        )
        return redirect("photoNotVerified")


def update_photo(request, photoID):
    # TODO Функция одобрения обновления фотографии (админка).
    """
    Функция из админки.
    Получаем фотографию, которой нужно заменить фотографию,
     если мы одобрили обновление
    То перезаписываем старую фотографию на новую,
     новую фотографию удаляем.
    Меняем state с Update на Verified.
    """
    UpdateOldPhotoOnNewPhotoService.execute(
        {"photo": get_object_or_404(Photo, id=photoID)}
    )
    return redirect("photoUpdate")
