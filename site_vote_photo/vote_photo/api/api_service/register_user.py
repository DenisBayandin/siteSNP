from django.core.exceptions import ValidationError
from service_objects.services import Service
from django import forms
from django.forms import ModelChoiceField

from vote_photo.models import User


class UserRegisterService(Service):
    user = ModelChoiceField(queryset=User.objects.all())
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    patronymic = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()

    def process(self):
        self.set_params_user(
            self.cleaned_data["user"],
            self.cleaned_data["username"],
            self.cleaned_data["first_name"],
            self.cleaned_data["last_name"],
            self.cleaned_data["patronymic"],
            self.cleaned_data["email"],
        )
        breakpoint()
        self.check_and_set_password(
            self.cleaned_data["password"],
            self.cleaned_data["password2"],
            self.cleaned_data["user"],
        )

    def set_params_user(self, user, username, first_name, last_name, patronymic, email):
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.patronymic = patronymic
        user.email = email
        user.save()

    def check_and_set_password(self, password, password2, user):
        if password != password2:
            raise ValidationError(
                {password: f"{password, password2} Пароли не совпадают."}
            )
        user.set_password(password)
        user.save()
