from service_objects.services import Service
from django.forms import ModelChoiceField
from rest_framework.authtoken.models import Token
from django import forms


from ..models import User


class ServiceRenameToken(Service):
    user = ModelChoiceField(queryset=User.objects.all())
    token = ModelChoiceField(queryset=Token.objects.all())

    def process(self):
        return self.rename_token(self.cleaned_data["token"], self.cleaned_data["user"])

    def rename_token(self, token, user):
        token.delete()
        return Token.objects.create(user=user)
