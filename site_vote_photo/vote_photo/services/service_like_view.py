from service_objects.services import Service
from django.forms import ModelChoiceField


from ..mymodels.model_like import Like
from ..mymodels.model_photo import Photo
from ..mymodels.model_user import User


class AddLikeService(Service):
    user = ModelChoiceField(queryset=User.objects.all())
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        photo = self.cleaned_data["photo"]
        return self.checking_like(photo, user)

    def checking_like(self, photo, user):
        if Like.objects.filter(photo=photo, user=user).exists():
            one_like_user = Like.objects.get(photo=photo, user=user)
            one_like_user.delete()
            return True
        else:
            photo = photo
            Like.objects.create(user=user, photo=photo)
            return False
