from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from vote_photo.mymodels.model_user import User


class RefreshTokenView(APIView):
    def put(self, request, format=None):
        try:
            user = User.objects.get(username=request.data["username"])
            if check_password(request.data["password"], user.password):
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
                user=user,
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": f"Token для {request.data['username']} не найден.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=404,
            )
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
