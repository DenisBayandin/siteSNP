from service_objects.services import Service
from django.forms import ModelChoiceField
from rest_framework.authtoken.models import Token
from django import forms


from ..mymodels.model_user import User


class ServiceRenameToken(Service):
    user = ModelChoiceField(queryset=User.objects.all())
    token = ModelChoiceField(queryset=Token.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        token = self.cleaned_data["token"]
        return self.rename_token(token, user)

    def rename_token(self, token, user):
        token.delete()
        return Token.objects.create(user=user)


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
