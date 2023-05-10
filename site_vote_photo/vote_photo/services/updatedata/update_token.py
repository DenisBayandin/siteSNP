from service_objects.services import Service
from service_objects.fields import ModelField
from rest_framework.authtoken.models import Token
from django import forms


from vote_photo.models import User


class ServiceRenameToken(Service):
    user = ModelField(User)
    token = ModelField(Token)

    def process(self):
        return self.rename_token(self.cleaned_data["token"], self.cleaned_data["user"])

    def rename_token(self, token, user):
        token.delete()
        return Token.objects.create(user=user)
