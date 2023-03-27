from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect

from ..models import Comment


def delete_comment(request, commentID, photoID):
    # TODO Функция удаления комментария.
    """
    Получаем комментарий, который хотим удалить.
    Если у комментария есть дети (у комментария есть ещё комментарии),
     то удалить невозможно.
    Иначе удаляем комментарий и уменьшаем на 1 общее кол-во комментариев
     на фотографии.
    """
    comment = get_object_or_404(Comment, id=commentID)
    for comment_children in Comment.objects.filter(parent=commentID):
        if comment_children.parent.id == comment.id:
            raise ValidationError("Невозможно удалить данный комментарий.")
    if request.user == comment.user:
        comment.delete()
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
