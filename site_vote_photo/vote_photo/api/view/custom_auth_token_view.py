from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class CustomGetAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
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
