from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.like import LikeSerializers
from vote_photo.models import *


class AllLikesOnePhotoView(APIView):
    @swagger_auto_schema(tags=["Like"], operation_description="View all like one photo")
    def get(self, request, photo_id, format=None):
        likes = Like.objects.filter(photo=photo_id)
        serializers = LikeSerializers(likes, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CreateLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        tags=["Like"],
        operation_description="Creating a like, if there is already a"
        " like on the photo, then delete the like.",
    )
    def post(self, request, photo_id, format=None, *args, **kwargs):
        try:
            like = Like.objects.get(photo=photo_id, user=request.user)
        except ObjectDoesNotExist:
            serializers = LikeSerializers(
                data=({"photo": photo_id, "user": request.user.id})
            )
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response(
            {
                "message": "Удалили лайк,"
                " так как вы пытаетесь создать лайк к фотографии,"
                " который уже существует у данного юзера.",
                "status": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class ChangeLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(tags=["Like"], operation_description="Get one like.")
    def get(self, request, photo_id, format=None):
        like = Like.objects.get(photo=photo_id, user=request.user.id)
        serializers = LikeSerializers(like)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Like"], operation_description="Delete ")
    def delete(self, request, photo_id, format=None):
        try:
            like = Like.objects.get(photo=photo_id, user=request.user)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": f"Вы не можете удалить лайк,"
                    f" так как у вас нет лайка на"
                    f" фотографии '{Photo.objects.get(id=photo_id).name}'.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
