from service_objects.services import Service
from django.forms import ModelChoiceField


from ..models import *


class AddLikeService(Service):
    user = ModelChoiceField(queryset=User.objects.all())
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        return self.checking_like(self.cleaned_data["photo"], self.cleaned_data["user"])

    def checking_like(self, photo, user):
        if Like.objects.filter(photo=photo, user=user).exists():
            one_like_user = Like.objects.get(photo=photo, user=user)
            one_like_user.delete()
            return True
        else:
            photo = photo
            Like.objects.create(user=user, photo=photo)
            return False
