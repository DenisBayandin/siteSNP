from service_objects.services import Service
from service_objects.fields import ModelField

from vote_photo.models import *


class CancelDeletePhotoService(Service):
    photo = ModelField(Photo)

    def process(self):
        self.change_date_and_state(self.cleaned_data["photo"])
        self.cleaned_data["photo"].save()

    def change_date_and_state(self, photo):
        photo.date_delete = None
        photo.go_state_not_verified()
