from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

from vote_photo.models import User
from rest_framework.authtoken.models import Token
from ..api_service.register_user import UserRegisterService


class UserRegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "photo_by_user",
            "password",
            "password2",
        ]

    def save(self, *args, **kwargs):
        user = User(
            username=self.validated_data["username"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            patronymic=self.validated_data["patronymic"],
            email=self.validated_data["email"],
            photo_by_user=self.validated_data["photo_by_user"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError(
                {password: f"{password, password2} Пароли не совпадают."}
            )
        user.set_password(password)
        user.save()
        return user


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "last_name",
            "first_name",
            "patronymic",
            "email",
            "photo_by_user",
        ]


class ChangeUserYesPassword(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=60)
    first_name = serializers.CharField(required=False, max_length=60)
    last_name = serializers.CharField(required=False, max_length=60)
    patronymic = serializers.CharField(required=False, max_length=60)
    email = serializers.EmailField(required=False, max_length=255)
    password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False, max_length=50)
    new_password2 = serializers.CharField(required=False, max_length=50)

    def update(self, instance, validated_data):
        if check_password(
            validated_data.get("password", instance.password), instance.password
        ):
            if (
                self.validated_data["new_password"]
                != self.validated_data["new_password2"]
            ):
                raise ValidationError(f"Новые пароли не совпадают. Попробуйте ещё раз.")
            instance.set_password(self.validated_data["new_password2"])
            instance.username = validated_data.get("username", instance.username)
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.patronymic = validated_data.get("patronymic", instance.patronymic)
            instance.email = validated_data.get("email", instance.email)
            instance.save()
            return instance
        else:
            raise ValidationError("Вы ввели не верный основной пароль.")
