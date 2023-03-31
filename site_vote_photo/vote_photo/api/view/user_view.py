from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

from ..serializers.user_serializers import (
    UserRegisterSerializers,
    UserSerializers,
    ChangeUserYesPassword,
)
from vote_photo.mymodels.model_user import User


class UsersView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializers = UserSerializers(users, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
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

    def get_objects(self, user_id):
        return get_object_or_404(User, id=user_id)

    def get(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        serializers = UserSerializers(user)
        return Response(serializers.data, status=status.HTTP_200_OK)

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
                    # breakpoint()
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

    def delete(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        if request.user.id != user_id:
            try:
                raise PermissionError(
                    f"У {request.user} нет полномочий удалять юзера '{user}'."
                )
            except PermissionError:
                return Response(
                    {
                        "error": f"У {request.user} нет полномочий удалять юзера '{user}'.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            token = Token.objects.get(user_id=user_id)
            token.delete()
            user.delete()
            return Response(
                {"status": status.HTTP_204_NO_CONTENT},
                status=status.HTTP_204_NO_CONTENT,
            )
