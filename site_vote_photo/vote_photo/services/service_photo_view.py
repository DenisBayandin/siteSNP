from django.db.models import Q
from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms

from ..mymodels.model_photo import Photo
from ..mymodels.model_user import User


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


class ServiceSortedPhotoOneUser(Service):
    sorted = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        sorted = self.cleaned_data["sorted"]
        user = self.cleaned_data["user"]
        photo_all = []
        if sorted == "All photo":
            return Photo.objects.filter(user=user.id)
        photo_one_user = Photo.objects.filter(user=user.id)
        for photo_one in photo_one_user:
            if photo_one.state == sorted:
                photo_all.append(photo_one)
        return photo_all


class ServiceMainSearchPhoto(Service):
    search = forms.CharField()

    def process(self):
        search = self.cleaned_data["search"]
        queryset_photo = Photo.objects.filter(
            (Q(name__icontains=search) | Q(content__icontains=search)),
            state="Verified",
        )
        return self.queryset_count(queryset_photo, search)

    def queryset_count(self, queryset, search):
        if queryset.count == 0:
            return self.if_count_queryset_like_0(search)
        elif User.objects.filter(username__icontains=search) != 0:
            return self.if_count_queryset_not_like_0(queryset, search)

    def if_count_queryset_like_0(self, search):
        photo_search = []
        user_search = User.objects.filter(username__icontains=search)
        if user_search != 0:
            for user_in_search in user_search:
                user_photo = Photo.objects.filter(
                    user=user_in_search.id, state="Verified"
                )
                for photo_one in user_photo:
                    photo_search.append(photo_one)
            return photo_search
        else:
            return None

    def if_count_queryset_not_like_0(self, queryset, search):
        photo_search_to_user = []
        user_search = User.objects.filter(username__icontains=search)
        for user_in_search in user_search:
            all_photo_to_one_user = Photo.objects.filter(
                user=user_in_search.id, state="Verified"
            )
            for one_photo_to_one_user in all_photo_to_one_user:
                photo_search_to_user.append(one_photo_to_one_user)
        set_gueryset = set(queryset)
        set_photo_search_to_user = set(photo_search_to_user)
        return list(set_gueryset.union(set_photo_search_to_user))
