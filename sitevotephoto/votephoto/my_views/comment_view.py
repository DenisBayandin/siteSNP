from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect

from ..models import *


def delete_comment(request, commentID, photoID):
    # TODO Функция удаления комментария.
    """
        Получаем комментарий, который хотим удалить.
        Если у комментария есть дети (у комментария есть ещё комментарии), то удалить невозможно.
        Иначе удаляем комментарий и уменьшаем на 1 общее кол-во комментариев на фотографии.
    """
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
    # TODO Функция изменения комментария.
    """
        Получаем комментарий, данные которого нужно поменять.
        Если текущей пользователь равен пользователю, который создал комментарий.
        То меняем содержимое комментария на новый текст, который пришёл в request.
    """
    comment = get_object_or_404(Comment, pk=commentID)
    if request.user == comment.user:
        val_comment = 'newComment' + str(commentID)
        if request.POST[val_comment] is not None:
            newContent = request.POST[val_comment]
            comment.content = newContent
            comment.save()
            return redirect('show_photo', photoID)
