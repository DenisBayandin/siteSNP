from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms

from ..models import *


class ServiceRenameProfile(Service):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    patronymic = forms.CharField()
    email = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.patronymic = self.cleaned_data["patronymic"]
        user.email = self.cleaned_data["email"]
        user.save()
