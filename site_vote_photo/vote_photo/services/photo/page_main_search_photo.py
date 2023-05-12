from django.db.models import Q
from service_objects.services import Service
from django import forms

from vote_photo.models import *


class ServiceMainSearchPhoto(Service):
    search = forms.CharField()

    def process(self):
        queryset_photo = Photo.objects.filter(
            (
                Q(name__icontains=self.cleaned_data["search"])
                | Q(content__icontains=self.cleaned_data["search"])
            ),
            state="Verified",
        )
        if self.queryset_count(queryset_photo, self.cleaned_data["search"]):
            return self.repay_photos_by_the_users_name(self.cleaned_data["search"])
        else:
            return self.repay_photos_by_the_users_name_a_also_name_and_content_photo(
                queryset_photo, self.cleaned_data["search"]
            )

    def queryset_count(self, queryset, search):
        if queryset.count == 0:
            return True
        elif User.objects.filter(username__icontains=search) != 0:
            return False

    def repay_photos_by_the_users_name(self, search):
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

    def repay_photos_by_the_users_name_a_also_name_and_content_photo(
        self, queryset, search
    ):
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
