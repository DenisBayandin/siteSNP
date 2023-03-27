from rest_framework import serializers

from vote_photo.mymodels.model_user import User


class UserRegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField()

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
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "photo_by_user",
            "is_superuser",
            "is_staff",
            "is_active",
        ]
