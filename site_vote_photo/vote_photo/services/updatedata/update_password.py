from service_objects.services import Service
from rest_framework import status
from service_objects.fields import ModelField
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from vote_photo.myexception.not_valided_password import UpdatePasswordExciption
from ...utils.services.custom_service import ServiceWithResult

from vote_photo.models import *


class ServiceUpdatePassword(ServiceWithResult):
    password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
    user = ModelField(User)

    custom_validations = ["validations_password"]

    def process(self):
        self.run_custom_validations()
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
        return self

    def check_password(self, password, new_password, new_password2, user):
        if check_password(password, user.password):
            if self.is_valid():
                if new_password != new_password2:
                    raise ValueError("Новые пароли не сходятся.")
                else:
                    return True
            else:
                raise ValidationError("Ввели не верный основной пароль.")

    def changing_the_password(self, user, new_password):
        user.set_password(new_password)

    def validations_password(self):
        if len(self.cleaned_data["new_password"]) < 8:
            self.add_error("id", "The password was not validated.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise UpdatePasswordExciption(
                self.cleaned_data["new_password"], "Пароль меньше 8 символов."
            )
        if len(self.cleaned_data["new_password"]) >= 20:
            self.add_error("id", "The password was not validated.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise UpdatePasswordExciption(
                self.cleaned_data["new_password"], "Пароль больше 20 символов."
            )
        # Пароль не схож с username.
        if self.cleaned_data["user"].username == self.cleaned_data["new_password"]:
            self.add_error("id", "The password was not validated.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise UpdatePasswordExciption(
                self.cleaned_data["new_password"], "Пароль схож с именем аккаунта."
            )
        # Пароль не состоит из одних лишь цифр.
        if self.cleaned_data["new_password"].isdigit():
            self.add_error("id", "The password was not validated.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise UpdatePasswordExciption(
                self.cleaned_data["new_password"], "Пароль из одних лишь цифр."
            )
        # Пароль не состоит из одних лишь букв.
        if self.cleaned_data["new_password"].isalpha():
            self.add_error("id", "The password was not validated.")
            self.response_status = status.HTTP_400_BAD_REQUEST
            raise UpdatePasswordExciption(
                self.cleaned_data["new_password"], "Пароль из одних лишь букв."
            )
        return True
