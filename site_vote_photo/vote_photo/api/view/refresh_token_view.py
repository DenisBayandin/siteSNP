from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from vote_photo.mymodels.model_user import User
from ..serializers.refresh_token_serializers import RefreshTokenSerializers


class RefreshTokenView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        request_body=RefreshTokenSerializers,
        tags=["token"],
        operation_description="Refresh TOKEN.",
    )
    def put(self, request, format=None):
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
