from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView

from vote_photo.models import User
from vote_photo.api.serializers.refresh_token import RefreshTokenSerializers


class RetrieveCreateCustomAuthTokenView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        tags=["Auth"],
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
