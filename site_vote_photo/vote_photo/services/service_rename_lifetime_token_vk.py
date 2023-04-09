from service_objects.services import Service
from django.forms import ModelChoiceField
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout


from ..mymodels.model_user import User


class ServiceRenameLifetimeTokenVk(Service):
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        if user.photo_by_user.name == "":
            return self.check_time_and_rename_token(user)

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
