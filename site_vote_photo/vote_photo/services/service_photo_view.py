from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms

from ..mymodels.model_photo import Photo


class LoadingNewDataService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    obj_name = forms.CharField()
    obj_content = forms.CharField()

    def process(self):
        photo = self.cleaned_data["photo"]
        obj_name = self.cleaned_data["obj_name"]
        obj_content = self.cleaned_data["obj_content"]
        self.change_data(photo, obj_name, obj_content)
        self.change_state(photo)

    def change_data(self, photo, obj_name, obj_content):
        photo.name = obj_name
        photo.content = obj_content

    def change_state(self, photo):
        photo.go_state_not_verified()
        photo.save()


class CancelDeletePhotoService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())

    def process(self):
        photo = self.cleaned_data["photo"]
        self.change_state(photo)
        self.change_date(photo)

    def change_date(self, photo):
        photo.date_delete = None
        photo.save()

    def change_state(self, photo):
        photo.go_state_not_verified()
