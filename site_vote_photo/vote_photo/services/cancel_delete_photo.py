from service_objects.services import Service
from django.forms import ModelChoiceField

from ..models import *


class CancelDeletePhotoService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        self.change_state(self.cleaned_data["photo"])
        self.change_date(self.cleaned_data["photo"])

    def change_date(self, photo):
        photo.date_delete = None
        photo.save()

    def change_state(self, photo):
        photo.go_state_not_verified()
