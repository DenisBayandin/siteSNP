from django.core.exceptions import ValidationError
from django.http import HttpResponse
from ...utils.errors.custom_error import ServiceObjectLogicError
from ...utils.services.custom_service import ServiceOutcome
from django.shortcuts import get_object_or_404, redirect

from vote_photo.services.comment.delete_comment import DeleteCommentService

from vote_photo.models import *


def delete_comment(request, commentID, photoID):
    # TODO Функция удаления комментария.
    """
    Получаем комментарий, который хотим удалить.
    Если у комментария есть дети (у комментария есть ещё комментарии),
     то удалить невозможно.
    Иначе удаляем комментарий и уменьшаем на 1 общее кол-во комментариев
     на фотографии.
    """
    try:
        outcome = ServiceOutcome(
            DeleteCommentService,
            {"comment": get_object_or_404(Comment, id=commentID), "user": request.user},
            request,
        )
    except ValidationError:
        return HttpResponse(
            "Не возможно удалить данные комментарий, так как имеются ответы."
        )
    return redirect("show_photo", photoID)


def update_comment(request, commentID, photoID):
    # TODO Функция изменения комментария.
    """
    Получаем комментарий, данные которого нужно поменять.
    Если текущей пользователь равен пользователю,
     который создал комментарий.
    То меняем содержимое комментария на новый текст,
     который пришёл в request.
    """
    comment = get_object_or_404(Comment, id=commentID)
    if request.user == comment.user:
        val_comment = "newComment" + str(commentID)
        if request.POST[val_comment] is not None:
            comment.content = request.POST[val_comment]
            comment.save()
            return redirect("show_photo", photoID)
