from service_objects.services import Service
from service_objects.fields import ModelField

from vote_photo.models import *


class ShowPhotoAdminService(Service):
    photo = ModelField(Photo)

    def process(self):
        return_photo = self.change_state(self.cleaned_data["photo"])
        return_photo.save()
        return return_photo

    def change_state(self, photo):
        if photo.state == "On check":
            photo.go_state_not_verified()
            photo.go_state_on_check()
            photo.save()
        else:
            photo.go_state_on_check()
            photo.save()
        return photo
