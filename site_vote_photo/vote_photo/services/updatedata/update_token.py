from service_objects.services import Service
from service_objects.fields import ModelField
from rest_framework.authtoken.models import Token


from vote_photo.models import User


class UpdateTokenService(Service):
    user = ModelField(User)
    token = ModelField(Token)

    def process(self):
        return self.update_token(self.cleaned_data["token"], self.cleaned_data["user"])

    def update_token(self, token, user):
        token.delete()
        return Token.objects.create(user=user)
