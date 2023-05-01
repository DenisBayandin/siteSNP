from service_objects.services import Service
from django.forms import ModelChoiceField
from datetime import timedelta
from django.utils import timezone


from vote_photo.models import User


class ServiceRenameLifetimeTokenVk(Service):
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        if self.cleaned_data["user"].photo_by_user.name == "":
            return self.check_time_and_rename_token(self.cleaned_data["user"])

    def check_time_and_rename_token(self, user):
        social = user.social_auth.get(provider="vk-oauth2")
        if (
            social.created + timedelta(seconds=social.extra_data["expires"])
            < timezone.now()
        ):
            social.created = social.modified
            social.save()
            return True
        else:
            return False
