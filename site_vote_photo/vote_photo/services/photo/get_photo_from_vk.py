import vk

from service_objects.services import Service
from service_objects.fields import ModelField

from vote_photo.models import User


version_vk_api = "5.131"


class ProfileGetPhotoFromVkService(Service):
    user = ModelField(User)

    def process(self):
        self.get_photo_from_vkontakte(self.cleaned_data["user"])
        self.cleaned_data["user"].save()

    def get_photo_from_vkontakte(self, user):
        social = user.social_auth.get(provider="vk-oauth2")
        api = vk.API(access_token=social.extra_data["access_token"], v=version_vk_api)
        json_vk = api.users.get(fields="photo_200")
        user.url_photo_by_user_from_VK = json_vk[0]["photo_200"]
