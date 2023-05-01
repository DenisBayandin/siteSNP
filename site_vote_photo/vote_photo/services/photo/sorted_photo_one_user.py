from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms

from vote_photo.models import *


class ServiceSortedPhotoOneUser(Service):
    sorted = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        photo_all = []
        if self.cleaned_data["sorted"] == "All photo":
            return Photo.objects.filter(user=self.cleaned_data["user"].id)
        photo_one_user = Photo.objects.filter(user=self.cleaned_data["user"].id)
        for photo_one in photo_one_user:
            if photo_one.state == self.cleaned_data["sorted"]:
                photo_all.append(photo_one)
        return photo_all
