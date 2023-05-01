from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms

from vote_photo.models import *


class LoadingNewDataService(Service):
    photo = ModelChoiceField(queryset=Photo.objects.all())
    obj_name = forms.CharField()
    obj_content = forms.CharField()

    def process(self):
        self.change_data(
            self.cleaned_data["photo"],
            self.cleaned_data["obj_name"],
            self.cleaned_data["obj_content"],
        )
        self.change_state(self.cleaned_data["photo"])
        self.cleaned_data["photo"].save()

    def change_data(self, photo, obj_name, obj_content):
        photo.name = obj_name
        photo.content = obj_content

    def change_state(self, photo):
        photo.go_state_not_verified()
