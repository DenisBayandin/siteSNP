import vk

from service_objects.services import Service
from django.forms import ModelChoiceField

from ..models import User


version_vk_api = "5.131"


class ProfileGetPhotoFromVkService(Service):
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        self.get_photo_from_vkontakte(self.cleaned_data["user"])

    def get_photo_from_vkontakte(self, user):
        social = user.social_auth.get(provider="vk-oauth2")
        api = vk.API(access_token=social.extra_data["access_token"], v=version_vk_api)
        json_vk = api.users.get(fields="photo_200")
        user.url_photo_by_user_from_VK = json_vk[0]["photo_200"]
        user.save()
