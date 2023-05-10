from django.shortcuts import get_object_or_404
from django_fsm import TransitionNotAllowed
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vote_photo.services.photo.save_photo_with_new_size import NewSizePhotoService
from vote_photo.models import Photo
from vote_photo.api.serializers.photo import AllPhotoSerializers


class AdminChangingStatePhotoView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)
    queryset = Photo.objects.all()
    lookup_field = "id"

    def get_objects(self, id):
        return get_object_or_404(Photo, id=id)

    def process_work(self, request, id, state, *args, **kwargs):
        photo = self.get_objects(id)
        try:
            if state == "not_verified":
                photo.go_state_not_verified()
            elif state == "verified":
                photo.go_state_verified()
            elif state == "update":
                photo.go_state_update()
            elif state == "on_check":
                photo.go_state_on_check()
            elif state == "delete":
                photo.go_state_photo_delete()
            else:
                try:
                    raise ValueError(f"{state} не существует такого состояния.")
                except ValueError:
                    return Response(
                        {
                            "error": f"Состояние {state} не найдено.",
                            "status": status.HTTP_404_NOT_FOUND,
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
        except TransitionNotAllowed:
            return Response(
                {
                    "error": f"Фотография '{photo.name}' находится в том же состояние"
                    f" на которое вы хотите поменять. "
                    f"Либо переход из данного {photo.state}"
                    f" состояния в состояние {state} невозможен.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        photo.save()
        serializers = AllPhotoSerializers(photo)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Admin"], operation_description="Changing the status of the photo."
    )
    def put(self, request, id, state, *args, **kwargs):
        return self.process_work(request, id, state)

    @swagger_auto_schema(
        tags=["Admin"], operation_description="Changing the status of the photo."
    )
    def patch(self, request, id, state, *args, **kwargs):
        return self.process_work(request, id, state)


class AdminUpdatePhotoView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)
    queryset = Photo.objects.all()
    lookup_field = "id"

    def update_photo(self, request, id, *args, **kwargs):
        photo = get_object_or_404(Photo, id=id)
        if photo.state == "Update":
            photo.old_photo = photo.new_photo
            photo.new_photo = None
            photo.go_state_verified()
            photo.save()
            NewSizePhotoService.execute({"photo": Photo.objects.get(id=id)})
            return Response(
                {"message": "Фотография обновлена.", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": f"Фотография '{photo.name}' не находится в состояние 'update'.",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        tags=["Admin"],
        operation_description="Approval of the photo modification."
        " We change the old photo to a new one and delete the photos,"
        " or change the photo data.",
    )
    def put(self, request, id, *args, **kwargs):
        return self.update_photo(request, id)

    @swagger_auto_schema(
        tags=["Admin"],
        operation_description="Approval of the photo modification."
        " We change the old photo to a new one and delete the photos,"
        " or change the photo data.",
    )
    def patch(self, request, id, *args, **kwargs):
        return self.update_photo(request, id)
