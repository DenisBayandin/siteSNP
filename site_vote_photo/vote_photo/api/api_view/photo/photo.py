from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from vote_photo.services.photo.save_photo_with_new_size import NewSizePhotoService
from vote_photo.models import Photo
from vote_photo.api.serializers.photo import (
    AllPhotoSerializers,
    LoadPhotoSerializers,
    UpdatePhotoYesPhotoSerializers,
    UpdatePhotoNoPhotoSerializers,
    UpdatePhotoSerializers,
)


class ListCreatePhotoView(ListCreateAPIView):
    parser_classes = (MultiPartParser,)
    queryset = Photo.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        tags=["Photo"],
        operation_description="View all photos with the status=Verified.",
    )
    def get(self, request):
        photo = Photo.objects.filter(state="Verified")
        serializers = AllPhotoSerializers(photo, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LoadPhotoSerializers,
        tags=["Photo"],
        operation_description="Creating a photo.",
    )
    def post(self, request, format=None, *args, **kwargs):
        try:
            token = request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            return Response(
                {
                    "message": "Учётные данные не были предоставлены.",
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = LoadPhotoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            NewSizePhotoService.execute(
                {"photo": Photo.objects.get(name=serializer.data["name"])}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyPhotoView(RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser,)
    queryset = Photo.objects.all()
    lookup_field = "id"

    def get_objects(self, id):
        return get_object_or_404(Photo, id=id)

    def update_state(self, id):
        photo = get_object_or_404(Photo, id=id)
        photo.go_state_update()
        photo.save()
        return 0

    def check_have_token(self, request):
        try:
            token = request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            raise KeyError

    def update_func(self, request, id, *args, **kwargs):
        try:
            self.check_have_token(request)
        except KeyError:
            return Response(
                {
                    "message": "Учётные данные не были предоставлены.",
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
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
            try:
                raise PermissionError(
                    f"У {request.user} нет полномочий изменять данную фотографию."
                )
            except PermissionError:
                return Response(
                    {
                        "message": "У {request.user} нет полномочий изменять данную фотографию.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @swagger_auto_schema(tags=["Photo"], operation_description="View one photo.")
    def get(self, request, id, format=None):
        photo = self.get_objects(id)
        serializers = AllPhotoSerializers(photo)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdatePhotoSerializers,
        tags=["Photo"],
        operation_description="Changing the data of the photo or the photo itself.",
    )
    def patch(self, request, id, format=None):
        return self.update_func(request, id)

    @swagger_auto_schema(
        request_body=UpdatePhotoSerializers,
        tags=["Photo"],
        operation_description="Changing the data of the photo or the photo itself.",
    )
    def put(self, request, id, format=None):
        return self.update_func(request, id)

    @swagger_auto_schema(tags=["Photo"], operation_description="Delete photo.")
    def delete(self, request, id, format=None):
        try:
            self.check_have_token(request)
        except KeyError:
            return Response(
                {
                    "message": "Учётные данные не были предоставлены.",
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
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


class ListPhotoFilterView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Photo.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        tags=["Photo"], operation_description="Filtering photos by status."
    )
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
