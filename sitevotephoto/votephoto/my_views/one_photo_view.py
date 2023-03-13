from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import *

channel_layer = get_channel_layer()


def showOnePhoto(request, photoID):
    # TODO Функция показа одной фотографии, и добавление комментария.
    """
        Получаем все комментарии к данной фотографии.
        Получаем все детские комментарии (комментарии к комментариям) к данной фотографии.
        Создаём комментарий, и добавляем +1 к общему кол-ву комментариев фотографии.
        Затем создаём уведомление о том, что добавлен комментарий к фотографии.
        Уведомление получает создать фотографии.
    """
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
            # TODO Нотификация о том, что некоторый пользователь оставил комментарий.
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


def loading_new_photo(request, photoID):
    # TODO Функция обновления фотографии или его содержимого.
    """
        Получаем фотографию, которую хотим изменить.
        Проверяем, если новая фотография не пришла, то скорей всего нужно изменить её содержимое ->
        -> получаем из формы данные и меняем содержимое фотографии на новые данные.
        Если же пришла фотография, то изменяем все данные фотографии, чтобы не делать новых проверок.
    """
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
    context = {
        'title': f'Обновление фотографии - {photo.name}',
        'form': form,
        'photo': photo
    }
    return render(request, 'votephoto/loadingNewPhoto.html', context)


def cancel_delete_photo(request, photoID):
    # TODO Функция отмены удаления фотографии.
    """
        Получаем фотографию, затем меняем state на Not verified
        Ставим поля date_now, date_delete на None
    """
    photo = get_object_or_404(Photo, pk=photoID)
    photo.go_state_not_verified()
    photo.date_now = None
    photo.date_delete = None
    photo.save()
    return redirect('all_photo')

