from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models

from ..serializers.comment_serializers import CommentSerializers
from vote_photo.mymodels.model_comment import Comment


class AllCommentOnePhotoView(APIView):
    def get(self, request, photo_id, format=None):
        comment = Comment.objects.filter(photo_id=photo_id)
        serializers = CommentSerializers(comment, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class OneCommentView(APIView):
    def get_objects(self, comment_id):
        return get_object_or_404(Comment, id=comment_id)

    def get(self, request, comment_id, format=None):
        comment = self.get_objects(comment_id)
        serializers = CommentSerializers(comment)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CreateCommentOnePhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, photo_id, *args, **kwargs):
        serializers = CommentSerializers(
            data=(request.data.dict() | {"photo": photo_id, "user": request.user.id})
        )
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


class СhangeOneCommentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def verification_of_credentials(self, request, comment):
        if request.user.id == comment.user.id:
            return True
        else:
            return False

    def get_objects(self, comment_id):
        return get_object_or_404(Comment, id=comment_id)

    def put(self, request, comment_id, format=None):
        comment = self.get_objects(comment_id)
        if self.verification_of_credentials(request, comment):
            serializers = CommentSerializers(comment, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                {
                    "error": f"У {request.user} нет полномочий производить какие-то"
                    f" манипуляции с данным комментарием.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, comment_id, format=None):
        try:
            comment = self.get_objects(comment_id)
            if not self.verification_of_credentials(request, comment):
                return Response(
                    {
                        "error": f"У {request.user} нет полномочий производить какие-то"
                        f" манипуляции с данным комментарием.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            comment.delete()
        except models.ProtectedError:
            return Response(
                {
                    "error": "Невозможно удалить комментарий. "
                    "Так как на данный коментарий есть ответы.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
