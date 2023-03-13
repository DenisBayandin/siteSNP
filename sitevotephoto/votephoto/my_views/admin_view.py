from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from ..models import *

channel_layer = get_channel_layer()


class ViewPhotoNotVerified(ListView):
    # TODO Отображение фотографий со статусом state=Not verified и state=On check (админка)
    """
        Объединяем фотографии с state=On check и state=Not verified с той целью,
        чтобы в случае чего, мы могли снова зайти на фотографию и посмотреть можем ли мы её одобрить.
        Ведь если мы захотим увидеть фотографии, которые требует проверки то мы увидим фотографии только с
        state=Not verified и в случае обновления страницы при проверке фотографии у нас будет вылетать ошибка.
    """
    template_name = 'votephoto/viewPhotoNotVerified.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка фотографий'
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            set_gueryset = set(Photo.objects.filter(state='Not verified'))
            set_photo_search_to_user = set(Photo.objects.filter(state='On check'))
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
            return super().get_queryset()
        else:
            raise Http404(f'{self.request.user.username} не является админом! Зайдите на другой аккаунт!')


class ViewPhotoUpdate(ListView):
    # TODO Отображение фотографий с state=Update (админка)
    template_name = 'votephoto/viewPhotoUpdate.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка фотографий'
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            self.queryset = Photo.objects.filter(state='Update')
            return super().get_queryset()
        else:
            raise Http404(f'{self.request.user.username} не является админом! Зайдите на другой аккаунт!')


class ViewPhotoDelete(ListView):
    # TODO Отображение фотографий с state=Delete (админка)
    template_name = 'votephoto/viewPhotoNotVerified.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка фотографий'
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            self.queryset = Photo.objects.filter(state='Delete')
            return super().get_queryset()
        else:
            raise Http404(f'{self.request.user.username} не является админом! Зайдите на другой аккаунт!')


def showPhotoAdmin(request, photoID):
    # TODO Функция проверки фотографии (админка)
    """
        Если пользователь имеет права админа, то провряем на наличие у фотографии state='On check'
        и отображаем фотографию
    """
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, pk=photoID)
        if photo.state == 'On check':
            photo.go_state_not_verified()
            photo.go_state_on_check()
            return render(request, 'votephoto/showPhotoAdmin.html', {
                'title': 'Проверка фотографии',
                'photo': photo
            })
        else:
            photo.go_state_on_check()
            photo.save()
            return render(request, 'votephoto/showPhotoAdmin.html', {
                'title': 'Проверка фотографии',
                'photo': photo
            })
    else:
        return Http404(Http404(f'{request.user.username} не является админом! Зайдите на другой аккаунт!'))


def showPhotoAdminUpdate(request, photoID):
    # TODO Функция отвечающая за проверку обновления (админка)
    """
        Проверяем если пользователь имеет права админа, то показыаем ему фотографию.
        Иначе ошибка (Http404).
    """
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, pk=photoID)
        photo.save()
        return render(request, 'votephoto/showPhotoAdminUpdate.html', {
            'title': 'Проверка фотографии',
            'photo': photo
        })
    else:
        return Http404(Http404(f'{request.user.username} не является админом! Зайдите на другой аккаунт!'))


def updateStateVerified(request, photoID):
    # TODO Функция меняющая state на Verified (админка)
    """
        Получаем фотографию.
        Меняем состояние фотографии на Verified.
        Создаём и отправляем увдомление создателю фотографии, что его фотография прошла проверку.
    """
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        photo.go_state_verified()
        photo.save()
        get_user_which_create_photo = photo.user_id
        get_user = User.objects.get(pk=get_user_which_create_photo)
        group_user_which_create_photo = get_user.group_name
        notification = Notification.objects.create()
        notification.message = f"Вашу фотографию '{photo.name}' одобрили."
        notification.save()
        async_to_sync(channel_layer.group_send)(group_user_which_create_photo, {
            "type": "send_new_data",
            "message": notification.message
        })
        return redirect('photoNotVerified')


def updateStateNotVerified(request, photoID):
    # TODO Функция меняющая state на Not verified (админка)
    """
        Получаем фотографию.
        Меняем состояние фотографии на Not verified.
        Создаём и отправляем увдомление создателю фотографии, что его фотография не прошла проверку.
    """
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        photo.go_state_not_verified()
        photo.save()
        get_user_which_create_photo = photo.user_id
        get_user = User.objects.get(pk=get_user_which_create_photo)
        group_user_which_create_photo = get_user.group_name
        notification = Notification.objects.create()
        notification.message = f"Вашу фотографию '{photo.name}' отклонили."
        notification.save()
        async_to_sync(channel_layer.group_send)(group_user_which_create_photo, {
            "type": "send_new_data",
            "message": notification.message
        })
        return redirect('photoNotVerified')


def update_photo(request, photoID):
    # TODO Функция одобрения обновления фотографии (админка).
    """
        Функция из админки.
        Получаем фотографию, которой нужно заменить фотографию, если мы одобрили обновление
        То перезаписываем старую фотографию на новую, новую фотографию удаляем.
        Меняем state с Update на Verified.
    """
    up_photo = get_object_or_404(Photo, pk=photoID)
    up_photo.old_photo = up_photo.new_photo
    up_photo.new_photo = None
    up_photo.go_state_verified()
    up_photo.save()
    return redirect('photoUpdate')
