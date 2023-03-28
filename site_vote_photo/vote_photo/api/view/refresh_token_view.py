from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from vote_photo.mymodels.model_user import User


class RefreshTokenView(APIView):
    def post(self, request, format=None):
        try:
            user = User.objects.get(username=request.data["username"])
            if check_password(request.data["password"], user.password):
                pass
            else:
                raise ValidationError("Не верный пароль.")
        except ObjectDoesNotExist:
            return Response(
                "Не найден пользователь, введите корректный username", status=404
            )
        except ValidationError:
            return Response(
                f"Не верный пароль {request.data['password']}."
                f" Попробуйте ввести другой пароль.",
                status=401,
            )
        try:
            token = Token.objects.get(
                user=user,
            )
        except ObjectDoesNotExist:
            return Response(
                f"Объект для {request.data['username']} не найден.", status=404
            )
        token.delete()
        return Response(
            {
                "new_token": Token.objects.create(
                    user=User.objects.get(username=request.data["username"])
                ).key,
                "username": request.data["username"],
            }
        )
