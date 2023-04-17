from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from ..models import *


class ServiceUpdatePassword(Service):
    password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        self.check_password(
            self.cleaned_data["password"],
            self.cleaned_data["new_password"],
            self.cleaned_data["new_password2"],
            self.cleaned_data["user"],
        )

    def check_password(self, password, new_password, new_password2, user):
        if check_password(password, user.password):
            if new_password != new_password2:
                raise ValueError("Новые пароли не сходятся.")
            else:
                self.changing_the_password(user, new_password)
        else:
            raise ValidationError("Ввели не верный основной пароль.")

    def changing_the_password(self, user, new_password):
        user.set_password(new_password)
        user.save()
