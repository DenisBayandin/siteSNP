from service_objects.services import Service
from service_objects.fields import ModelField
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from vote_photo.myexception.not_valided_password import UpdatePasswordExciption

from vote_photo.models import *


class ServiceUpdatePassword(Service):
    password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
    user = ModelField(User)

    def process(self):
        if self.check_password(
            self.cleaned_data["password"],
            self.cleaned_data["new_password"],
            self.cleaned_data["new_password2"],
            self.cleaned_data["user"],
        ):
            self.changing_the_password(
                self.cleaned_data["user"], self.cleaned_data["new_password"]
            )
        self.cleaned_data["user"].save()

    def check_password(self, password, new_password, new_password2, user):
        if check_password(password, user.password):
            if self.validations(user, new_password):
                if new_password != new_password2:
                    raise ValueError("Новые пароли не сходятся.")
                else:
                    return True
            else:
                raise ValidationError("Ввели не верный основной пароль.")

    def changing_the_password(self, user, new_password):
        user.set_password(new_password)

    def validations(self, user, password):
        print(len(password))
        if len(password) < 8:
            raise UpdatePasswordExciption(password, "Пароль меньше 8 символов.")
        if len(password) >= 20:
            raise UpdatePasswordExciption(password, "Пароль больше 20 символов.")
        # Пароль не схож с username.
        if user.username == password:
            raise UpdatePasswordExciption(password, "Пароль схож с именем аккаунта.")
        # Пароль не состоит из одних лишь цифр.
        if password.isdigit():
            raise UpdatePasswordExciption(password, "Пароль из одних лишь цифр.")
        # Пароль не состоит из одних лишь букв.
        if password.isalpha():
            raise UpdatePasswordExciption(password, "Пароль из одних лишь букв.")
        return True
