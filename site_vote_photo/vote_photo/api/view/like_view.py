from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.like_serializers import LikeSerializers
from vote_photo.mymodels.model_like import Like
from vote_photo.mymodels.model_photo import Photo


class AllLikesOnePhotoView(APIView):
    def get(self, request, photo_id, format=None):
        likes = Like.objects.filter(photo=photo_id)
        serializers = LikeSerializers(likes, many=True)
        return Response(serializers.data)


class CreateLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, photo_id, *args, **kwargs):
        try:
            like = Like.objects.get(photo=photo_id, user=request.user)
        except ObjectDoesNotExist:
            serializers = LikeSerializers(
                data=({"photo": photo_id, "user": request.user.id})
            )
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors)
        like.delete()
        return Response(
            "Удалили лайк,"
            " так как вы пытаетесь создать лайк к фотографии,"
            " который уже существует у данного юзера."
        )


class ChangeLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, photo_id, format=None):
        like = Like.objects.get(photo=photo_id, user=request.user.id)
        serializers = LikeSerializers(like)
        return Response(serializers.data)

    def delete(self, request, photo_id, format=None):
        try:
            like = Like.objects.get(photo=photo_id, user=request.user)
        except ObjectDoesNotExist:
            return Response(
                f"Вы не можете удалить лайк,"
                f" так как у вас нет лайка на фотографии '{Photo.objects.get(id=photo_id).name}'.",
                status=status.HTTP_404_NOT_FOUND,
            )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
