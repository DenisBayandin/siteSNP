import json
from datetime import datetime, timedelta

import vk
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, ListView
from rest_framework.authtoken.models import Token

from .forms import *

version_vk_api = '5.131'
channel_layer = get_channel_layer()


class RegisterUser(CreateView):
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
    form_class = LoginUsersForm
    template_name = 'votephoto/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class MainView(ListView):
    template_name = 'votephoto/main.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        self.queryset = Photo.objects.filter(state='Verified')
        return super().get_queryset()


class MainSortedView(ListView):
    template_name = 'votephoto/sortedMain.html'
    context_object_name = 'photo'

    def get_queryset(self):
        get_sorted_name = self.kwargs.get('sorting')
        self.queryset = Photo.objects.filter(state='Verified').order_by(get_sorted_name)
        return super().get_queryset()


class MainSearchView(ListView):
    template_name = 'votephoto/searchMain.html'
    context_object_name = 'photo'

    def get_queryset(self):
        what_wrote_to_user = self.kwargs.get('search')
        self.queryset = Photo.objects.filter(
            (Q(name__icontains=what_wrote_to_user) | Q(content__icontains=what_wrote_to_user)), state='Verified')
        if self.queryset.count() == 0:
            photo_search = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            if user_search != 0:
                for user_in_search in user_search:
                    user_photo = Photo.objects.filter(user=user_in_search.pk, state='Verified')
                    for photo_one in user_photo:
                        photo_search.append(photo_one)
                self.queryset = photo_search
            else:
                self.queryset = None
        elif User.objects.filter(username__icontains=what_wrote_to_user) != 0:
            photo_search_to_user = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            for user_in_search in user_search:
                all_photo_to_one_user = Photo.objects.filter(user=user_in_search.pk, state='Verified')
                for one_photo_to_one_user in all_photo_to_one_user:
                    photo_search_to_user.append(one_photo_to_one_user)
            set_gueryset = set(self.queryset)
            set_photo_search_to_user = set(photo_search_to_user)
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
        else:
            self.queryset = None
        return super().get_queryset()


class SortedAllPhotoOneUser(ListView):
    template_name = 'votephoto/sortedAllPhotoOneUser.html'
    context_object_name = 'photo'

    def get_queryset(self):
        photo_all = []
        get_sorted_name = self.kwargs.get('sorting')
        if get_sorted_name == 'All photo':
            self.queryset = Photo.objects.filter(user=self.request.user.pk)
            return super().get_queryset()
        photo_one_user = Photo.objects.filter(user=self.request.user.pk)
        for photo_one in photo_one_user:
            if photo_one.state == get_sorted_name:
                photo_all.append(photo_one)
        self.queryset = list(set(photo_all))
        return super().get_queryset()


class ViewPhotoNotVerified(ListView):
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
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, pk=photoID)
        if photo.state == 'On check':
            photo.go_state_not_verified()
            photo.go_state_on_check()
            return render(request, 'votephoto/showPhotoAdmin.html', {'title': 'Проверка фотографии', 'photo': photo})
        else:
            photo.go_state_on_check()
            photo.save()
            return render(request, 'votephoto/showPhotoAdmin.html', {'title': 'Проверка фотографии', 'photo': photo})
    else:
        return Http404(Http404(f'{request.user.username} не является админом! Зайдите на другой аккаунт!'))


def showPhotoAdminUpdate(request, photoID):
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, pk=photoID)
        photo.save()
        return render(request, 'votephoto/showPhotoAdminUpdate.html', {'title': 'Проверка фотографии', 'photo': photo})
    else:
        return Http404(Http404(f'{request.user.username} не является админом! Зайдите на другой аккаунт!'))


def updateStateVerified(request, photoID):
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


def showOnePhoto(request, photoID):
    comment_show = Comment.objects.filter(photo=photoID, Parent=None)
    commentChildren_show = Comment.objects.exclude(Parent=None).filter(photo=photoID)
    try:
        photo = get_object_or_404(Photo, pk=photoID)
    except:
        raise Http404(f'Фотографии {photoID} не существует')
    # if request.user.is_authenticated:
    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.POST.get("answer", None):
                id = int(request.POST.get("answer"))
                obj.Parent = Comment.objects.get(pk=id)
            # else:
            #     raise Http404()
            obj.user = request.user
            obj.photo = photo
            obj.save()
            add_comment_to_photo = Photo.objects.get(pk=photoID)
            add_comment_to_photo.count_comment += 1
            add_comment_to_photo.save()
            pk_user_create_photo = add_comment_to_photo.user_id
            get_user_create_photo = User.objects.get(pk=pk_user_create_photo)
            group_user_which_create_photo = get_user_create_photo.group_name
            user_create_notification = request.user
            notification = Notification.objects.create(sender=user_create_notification)
            notification.message = f'Пользователь {notification.sender} оставил ' \
                                   f'комментарий под фотографией: {add_comment_to_photo.name}' \
                                   f'\nОбщее кол-во комментариев на фотографии: {add_comment_to_photo.count_comment}'
            notification.save()
            async_to_sync(channel_layer.group_send)(group_user_which_create_photo, {
                "type": "send_new_data",
                "message": notification.message
            })
            return redirect(photo.get_absolute_url())
    else:
        form = AddComment
    return render(request, 'votephoto/showOnePhoto.html',
                  {'form': form,
                   'photo': photo,
                   'title': photo.name,
                   'show_comments': comment_show,
                   'show_children_comment': commentChildren_show})


def update_photo(request, photoID):
    up_photo = get_object_or_404(Photo, pk=photoID)
    up_photo.old_photo = up_photo.new_photo
    up_photo.new_photo = None
    up_photo.go_state_verified()
    up_photo.save()
    return redirect('photoUpdate')


def loading_new_photo(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        form = AddNewPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if form.data.get('new_photo') == '':
                photo.name = obj.name
                photo.content = obj.content
                photo.go_state_not_verified()
                photo.save()
                return redirect('all_photo')
            else:
                photo.name = obj.name
                photo.content = obj.content
                photo.new_photo = obj.new_photo
                photo.go_state_update()
                photo.save()
                return redirect('all_photo')
    else:
        form = AddNewPhotoForm
    context = {'title': f'Обновление фотографии - {photo.name}', 'form': form, 'photo': photo}
    return render(request, 'votephoto/loadingNewPhoto.html', context)


def delete_comment(request, commentID, photoID):
    comment = get_object_or_404(Comment, pk=commentID)
    comment_children_all = Comment.objects.filter(Parent=commentID)
    for comment_children in comment_children_all:
        if comment_children.Parent.pk == comment.pk:
            raise ValidationError("Невозможно удалить данный комментарий.")
    if request.user == comment.user:
        comment.delete()
        remove_comment_to_photo = Photo.objects.get(pk=photoID)
        remove_comment_to_photo.count_comment -= 1
        remove_comment_to_photo.save()
        return redirect('show_photo', photoID)


def update_comment(request, commentID, photoID):
    comment = get_object_or_404(Comment, pk=commentID)
    if request.user == comment.user:
        val_comment = 'newComment' + str(commentID)
        if request.POST[val_comment] is not None:
            newContent = request.POST[val_comment]
            comment.content = newContent
            comment.save()
            return redirect('show_photo', photoID)


def profile(request):
    """
        Функция профиля.
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
    return render(request, 'votephoto/profile.html', {'form': form,
                                                      'title': 'Личный кабинет',
                                                      'token': token})


def logout_view(request):
    logout(request)
    return redirect('main')


def addlike(request):
    """
        Функция создания и удаления лайка.
        Сперва получаем ID фотографии
        Затем проверяем, поставил ли пользователь лайк на нашу фотографию
        Если да, то получаем лайк, удаляем его и уменьшем кол-во лайков на 1, отправляем status 200
        Если нет, получаем фотографию, создаём лайк и передаём пользователя и фотографию,
        а после этого увеличиваем кол-во лайков на 1 и отправляем status 200
    """
    if request.user.is_authenticated:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        data = json.load(request)
        photoID = data.get('photoID')
        if is_ajax:
            if request.method == 'POST':
                if Like.objects.filter(photo=photoID, user=request.user).exists():
                    one_like_user = Like.objects.get(photo=photoID, user=request.user)
                    one_like_user.delete()
                    remove_like_to_photo = Photo.objects.get(pk=photoID)
                    remove_like_to_photo.count_like -= 1
                    remove_like_to_photo.save()
                    return HttpResponse(status=200)
                else:
                    photo = get_object_or_404(Photo, pk=photoID)
                    like = Like()
                    like.user = request.user
                    like.photo = photo
                    like.save()
                    add_like_to_photo = Photo.objects.get(pk=photoID)
                    add_like_to_photo.count_like += 1
                    add_like_to_photo.save()
                    return HttpResponse(status=201)
        else:
            return HttpResponse("Ошибка.", status=400, reason='Invalid request')
    else:
        return HttpResponse(status=202)


def viewAllPhoto(request):
    """
        Все фотографии одного пользователя.
        Получаем фотографии текущего пользователя.
    """

    photos = Photo.objects.filter(user=request.user)
    context = {'title': f'Фотографии {request.user.username}-a', 'photo': photos}
    return render(request, 'votephoto/allPhotoOneUser.html', context)


@shared_task(name="celery_delete_photo")
def celery_delete_photo():
    """
        Получаем фотографии со state = Delete и их количество
        После чего для каждой такой фотографии меняем поле date_now на текущее время
        Далее проверяем, если текущее время больше времени, когда фотографию нужно удалить,
        То фотографию удаляем.
    """
    photo_delete_all = Photo.objects.filter(state='Delete')
    count_photo_delete = Photo.objects.filter(state='Delete').count()
    for one_photo_delete in photo_delete_all:
        one_photo_delete.date_now = timezone.now()
        one_photo_delete.save()
        if one_photo_delete.date_now >= one_photo_delete.date_delete:
            one_photo_delete.delete()
    if count_photo_delete >= 1:
        return 'There are photos to delete.'
    else:
        return 'No photos to delete.'


def delete_photo(request, photoID):
    """
        Функция получает фотографию, после чего заносит в БД данные о времени, когда её нужно удалить
        меняет state на delete.
    """
    photo = get_object_or_404(Photo, pk=photoID)
    photo.date_delete = datetime.now() + timedelta(minutes=15)
    photo.date_now = datetime.now() + timedelta(seconds=1)
    photo.go_state_photo_delete()
    photo.save()
    # TODO Отправка уведомлений тем, у кого есть комментарии к этой фотографии.
    get_coment_to_the_photo = Comment.objects.filter(photo_id=photo.pk)
    check_send_notification = []
    for comment in get_coment_to_the_photo:
        get_user = User.objects.get(pk=comment.user_id)
        if get_user.pk in check_send_notification:
            continue
        else:
            check_send_notification.append(get_user.pk)
            group_name_to_create_comment = get_user.group_name
            notification_comment_on_the_photo_delete = Notification.objects.create()
            notification_comment_on_the_photo_delete.message = f"Ваш/Ваши комментарий/комментарии " \
                                                               f"к фотографии '{photo.name}' " \
                                                               f"скоро будет/будут удалён/удалены, так как " \
                                                               f"фотография отправлена на удаление."
            notification_comment_on_the_photo_delete.save()
            async_to_sync(channel_layer.group_send)(group_name_to_create_comment, {
                "type": "send_new_data",
                "message": notification_comment_on_the_photo_delete.message
            })
    return redirect('all_photo')


def cancel_delete_photo(request, photoID):
    """
        Функция отмены удаления фотографии.
        Получаем фотографию, затем меняем state на Not verified
        Ставим поля date_now, date_delete на None
    """
    photo = get_object_or_404(Photo, pk=photoID)
    photo.go_state_not_verified()
    photo.date_now = None
    photo.date_delete = None
    photo.save()
    return redirect('all_photo')


def rename_token(request):
    """
        Функция генерирования нового токена.
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
    """
        Функция для переименования данных в профиле.
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
