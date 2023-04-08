from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser


from ..serializers.user_serializers import (
    UserRegisterSerializers,
    UserSerializers,
    ChangeUserYesPassword,
)
from vote_photo.mymodels.model_user import User


class UsersView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(tags=["User"], operation_description="View all users.")
    def get(self, request, format=None):
        users = User.objects.all()
        serializers = UserSerializers(users, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserRegisterSerializers,
        tags=["User"],
        operation_description="Creating a new user.",
    )
    def post(self, request, format=None, *args, **kwargs):
        serializers = UserRegisterSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            breakpoint()
            Token.objects.create(
                user_id=User.objects.get(username=request.data["username"]).id
            )
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUser(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    def get_objects(self, user_id):
        return get_object_or_404(User, id=user_id)

    @swagger_auto_schema(tags=["User"], operation_description="View one user.")
    def get(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        serializers = UserSerializers(user)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChangeUserYesPassword,
        tags=["User"],
        operation_description="Changing user data.",
    )
    def put(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        if request.user.id != user_id:
            try:
                raise PermissionError(
                    f"У {request.user} нет полномочий изменять юзера '{user}'."
                )
            except PermissionError:
                return Response(
                    {
                        "error": f"У {request.user} нет полномочий изменять юзера '{user}'.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            try:
                old_password = request.data["password"]
                serializers = ChangeUserYesPassword(
                    data=(
                        request.data.dict()
                        | {"token": Token.objects.get(user=request.user.id).key}
                    )
                )
            except MultiValueDictKeyError:
                serializers = UserSerializers(user, data=request.data)
            if serializers.is_valid():
                try:
                    serializers.update(user, validated_data=request.data)
                except ValidationError:
                    return Response(
                        {
                            "error": "Введённые данные некорректны.",
                            "status": status.HTTP_400_BAD_REQUEST,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
