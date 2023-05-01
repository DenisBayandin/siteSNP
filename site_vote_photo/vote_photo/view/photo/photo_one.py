from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404, redirect, render
from channels.layers import get_channel_layer

from vote_photo.forms import AddComment, AddNewPhotoForm
from vote_photo.models import Comment, Photo
from vote_photo.view.update.update_token_by_vk import rename_lifetime_token_vk
from vote_photo.services.comment.send_notification_about_create_comment import (
    SendNotificationCommentService,
)
from vote_photo.services.photo.cancel_delete_photo import CancelDeletePhotoService

channel_layer = get_channel_layer()


def show_one_photo(request, photoID):
    # TODO Функция показа одной фотографии, и добавление комментария.
    """
    Получаем все комментарии к данной фотографии.
    Получаем все детские комментарии (комментарии к комментариям)
     к данной фотографии.
    Создаём комментарий, и добавляем +1 к общему кол-ву
     комментариев фотографии.
    Затем создаём уведомление о том, что добавлен
     комментарий к фотографии.
    Уведомление получает создать фотографии.
    """
    if request.user != AnonymousUser():
        if rename_lifetime_token_vk(request, request.user):
            return redirect("login")
    comment_show = Comment.objects.filter(photo=photoID, parent=None)
    comment_children_show = Comment.objects.exclude(parent=None).filter(photo=photoID)
    photo = get_object_or_404(Photo, id=photoID)
    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.POST.get("answer", None):
                obj.parent = Comment.objects.get(id=int(request.POST.get("answer")))
            obj.user = request.user
            obj.photo = photo
            obj.save()
            # TODO Нотификация о том,
            #  что некоторый пользователь оставил комментарий.
            SendNotificationCommentService.execute(
                {"user": request.user, "photo": photo}
            )
            return redirect(photo.get_absolute_url())
    else:
        form = AddComment
    return render(
        request,
        "vote_photo/showOnePhoto.html",
        {
            "form": form,
            "photo": photo,
            "title": photo.name,
            "show_comments": comment_show,
            "show_children_comment": comment_children_show,
        },
    )


def loading_new_photo(request, photoID):
    # TODO Функция обновления фотографии или его содержимого.
    """
    Получаем фотографию, которую хотим изменить.
    Проверяем, если новая фотография не пришла,
     то скорей всего нужно изменить её содержимое ->
    -> получаем из формы данные и меняем содержимое
     фотографии на новые данные.
    Если же пришла фотография, то изменяем все данные фотографии,
     чтобы не делать новых проверок.
    """
    photo = get_object_or_404(Photo, id=photoID)
    if request.method == "POST":
        form = AddNewPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if form.data.get("new_photo") == "":
                photo.name = obj.name
                photo.content = obj.content
                photo.go_state_not_verified()
                photo.save()
                return redirect("all_photo")
            else:
                photo.name = obj.name
                photo.content = obj.content
                photo.new_photo = obj.new_photo
                photo.go_state_update()
                photo.save()
                return redirect("all_photo")
    else:
        form = AddNewPhotoForm
    context = {
        "title": f"Обновление фотографии - {photo.name}",
        "form": form,
        "photo": photo,
    }
    return render(request, "vote_photo/loadingNewPhoto.html", context)


def cancel_delete_photo(request, photoID):
    # TODO Функция отмены удаления фотографии.
    """
    Получаем фотографию, затем меняем state на Not verified
    Ставим поля date_now, date_delete на None
    """
    CancelDeletePhotoService.execute({"photo": get_object_or_404(Photo, id=photoID)})
    return redirect("all_photo")
