from service_objects.services import Service
from service_objects.fields import ModelField
from django import forms

from vote_photo.models import *


class ServiceSortedPhotoOneUser(Service):
    sorted = forms.CharField()
    user = ModelField(User)

    def process(self):
        return self.return_sorted_photo(
            self.cleaned_data["sorted"], self.cleaned_data["user"]
        )

    def return_sorted_photo(self, sorted, user):
        photo_all = []
        if sorted == "All photo":
            return Photo.objects.filter(user=user.id)
        photo_one_user = Photo.objects.filter(user=user.id)
        for photo_one in photo_one_user:
            if photo_one.state == sorted:
                photo_all.append(photo_one)
        return photo_all
