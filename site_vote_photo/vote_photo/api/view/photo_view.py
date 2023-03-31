from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vote_photo.mymodels.model_photo import Photo
from ..serializers.photo_serializers import (
    AllPhotoSerializers,
    LoadPhotoSerializers,
    UpdatePhotoYesPhotoSerializers,
    UpdatePhotoNoPhotoSerializers,
)


class AllPhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        photo = Photo.objects.all()
        serializers = AllPhotoSerializers(photo, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = LoadPhotoSerializers(
            data=(request.data.dict() | {"user": request.user.id})
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class СhangeOnePhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_objects(self, id):
        return get_object_or_404(Photo, id=id)

    def update_state(self, id):
        photo = get_object_or_404(Photo, id=id)
        photo.go_state_update()
        photo.save()
        return 0

    def get(self, request, id, format=None):
        photo = self.get_objects(id)
        serializers = AllPhotoSerializers(photo)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        photo = self.get_objects(id)
        if request.user.id == photo.user.id:
            try:
                image = request.data["new_photo"]
                serializers = UpdatePhotoYesPhotoSerializers(photo, data=request.data)
            except MultiValueDictKeyError:
                serializers = UpdatePhotoNoPhotoSerializers(photo, data=request.data)
            if serializers.is_valid():
                serializers.save()
                self.update_state(id)
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionError(
                f"У {request.user} нет полномочий изменять данную фотографию."
            )

    def delete(self, request, id, format=None):
        photo = self.get_objects(id)
        if request.user.id == photo.user.id:
            serializers = AllPhotoSerializers(photo)
            photo.go_state_photo_delete()
            photo.save()
            return Response(serializers.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "error": f"У {request.user} нет полномочий удалять данную фотографию.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class PhotosUserFilter(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, filter, format=None):
        filters = {
            "verified": "Verified",
            "not_verified": "Not verified",
            "update": "Update",
            "delete": "Delete",
            "on_check": "On check",
        }
        try:
            photos = Photo.objects.filter(state=filters[filter], user=request.user)
        except KeyError:
            return Response(
                {
                    "error": "Введите другой фильтр, доступные фильтры: "
                    "1) verified 2) not_verified 3) update "
                    "4) delete 5) on_check. Пример запроса: .../api/user/photos/verified/",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializers = AllPhotoSerializers(photos, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class AllPhotoWithStateVerifiedView(APIView):
    def get(self, request, format=None):
        photo = Photo.objects.filter(state="Verified")
        serializers = AllPhotoSerializers(photo, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class GetOnePhotoView(APIView):
    def get_objects(self, id):
        return get_object_or_404(Photo, id=id)

    def get(self, request, photo_id, format=None):
        photo = self.get_objects(photo_id)
        serializers = AllPhotoSerializers(photo)
        return Response(serializers.data, status=status.HTTP_200_OK)
