from service_objects.services import Service
from service_objects.fields import ModelField


from vote_photo.models import *


class AddLikeService(Service):
    user = ModelField(User)
    photo = ModelField(Photo)

    def process(self):
        return self.create_or_delete_like(
            self.cleaned_data["photo"], self.cleaned_data["user"]
        )

    def create_or_delete_like(self, photo, user):
        if Like.objects.filter(photo=photo, user=user).exists():
            one_like_user = Like.objects.get(photo=photo, user=user)
            one_like_user.delete()
            return True
        else:
            Like.objects.create(user=user, photo=photo)
            return False
