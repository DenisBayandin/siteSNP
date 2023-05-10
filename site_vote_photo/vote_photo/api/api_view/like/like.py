from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    GenericAPIView,
    get_object_or_404,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from vote_photo.api.serializers.like import LikeSerializers
from vote_photo.models import *


class ListPhotoLikeView(ListAPIView):
    serializer_class = LikeSerializers
    lookup_field = "id"

    @swagger_auto_schema(tags=["Like"], operation_description="View all like one photo")
    def get(self, request, id, format=None):
        likes = Like.objects.filter(photo=id)
        serializers = LikeSerializers(likes, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CreateLikeView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        tags=["Like"],
        operation_description="Creating a like, if there is already a"
        " like on the photo, then delete the like.",
    )
    def post(self, request, id, *args, **kwargs):
        photo = get_object_or_404(Photo, id=id)
        try:
            like = Like.objects.get(photo=id, user=request.user)
        except ObjectDoesNotExist:
            serializers = LikeSerializers(data=({"photo": id, "user": request.user.id}))
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": "Лайк к данной фотографии у данного юзера уже существует."
                " Невозможно создать лайк.",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(tags=["Like"], operation_description="Delete like.")
    def delete(self, request, id, format=None):
        photo = get_object_or_404(Photo, id=id)
        try:
            like = Like.objects.get(photo=id, user=request.user)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": f"Вы не можете удалить лайк,"
                    f" так как у вас нет лайка на"
                    f" фотографии '{Photo.objects.get(id=id).name}'.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
