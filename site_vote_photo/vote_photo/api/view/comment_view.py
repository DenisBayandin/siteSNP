from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models

from ..serializers.comment_serializers import CommentSerializers
from vote_photo.mymodels.model_comment import Comment


class CommentOnePhotoView(APIView):
    def get(self, request, photo_id, format=None):
        comment = Comment.objects.filter(photo_id=photo_id)
        serializers = CommentSerializers(comment, many=True)
        return Response(serializers.data)

    def post(self, request, photo_id, *args, **kwargs):
        serializers = CommentSerializers(
            data=(request.data.dict() | {"photo": photo_id})
        )
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.data, status=400)


class OneCommentView(APIView):
    def get_objects(self, comment_id):
        return get_object_or_404(Comment, id=comment_id)

    def get(self, request, comment_id, format=None):
        comment = self.get_objects(comment_id)
        serializers = CommentSerializers(comment)
        return Response(serializers.data)

    def put(self, request, comment_id, format=None):
        comment = self.get_objects(comment_id)
        serializers = CommentSerializers(comment, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=401)

    def delete(self, request, comment_id, format=None):
        try:
            comment = self.get_objects(comment_id)
            comment.delete()
        except models.ProtectedError:
            return Response(
                "Невозможно удалить комментарий. Так как на данный коментарий есть ответы."
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
