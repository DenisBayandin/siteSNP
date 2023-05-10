from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import check_password

from vote_photo.models import User
from vote_photo.api.serializers.refresh_token import RefreshTokenSerializers


class RetrieveCreateCustomAuthTokenView(
    mixins.RetrieveModelMixin, generics.CreateAPIView
):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        tags=["Token"],
        operation_description="If the user has logged into the session,"
        " then we just get a TOKEN, otherwise BAD REQUEST",
    )
    def get(self, request, *args, **kwargs):
        if request.user == AnonymousUser():
            return Response(
                {
                    "error": "Не возможно получить токен AnonymousUser, войдите в профиль.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = Token.objects.get_or_create(user=request.user.id)
        return Response(
            {
                "token": token[0].key,
                "username": request.user.username,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=RefreshTokenSerializers,
        tags=["Token"],
        operation_description="Refresh TOKEN.",
    )
    def post(self, request, format=None):
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
        try:
            user_get_request = User.objects.get(username=request.data["username"])
            if check_password(request.data["password"], user_get_request.password):
                pass
            else:
                raise ValidationError("Не верный пароль.")
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "Не найден пользователь, введите корректный username",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError:
            return Response(
                {
                    "error": f"Не верный пароль {request.data['password']}."
                    f" Попробуйте ввести другой пароль.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = Token.objects.get(
                user=user_get_request.id,
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": f"Token для {request.data['username']} не найден.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=404,
            )
        if request.user == user_get_request:
            token.delete()
            return Response(
                {
                    "new_token": Token.objects.create(
                        user=User.objects.get(username=request.data["username"])
                    ).key,
                    "username": request.data["username"],
                    "status": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": f"Вы не можете изменить токен '{user_get_request.username}'.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
