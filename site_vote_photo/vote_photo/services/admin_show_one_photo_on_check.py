from service_objects.services import Service
from django.forms import ModelChoiceField

from ..models import *


class ShowPhotoAdminService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        return self.change_state(self.cleaned_data["photo"])

    def change_state(self, photo):
        if photo.state == "On check":
            photo.go_state_not_verified()
            photo.go_state_on_check()
            photo.save()
        else:
            photo.go_state_on_check()
            photo.save()
        return photo
