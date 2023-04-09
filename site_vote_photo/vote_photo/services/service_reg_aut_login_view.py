import vk

from django.core.exceptions import ValidationError
from service_objects.services import Service
from django.forms import ModelChoiceField
from django import forms
from django.contrib.auth.hashers import check_password


from ..mymodels.model_user import User


version_vk_api = "5.131"


class ProfileGetPhotoFromVkService(Service):
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        user = self.cleaned_data["user"]
        self.get_photo_from_vkontakte(user)

    def get_photo_from_vkontakte(self, user):
        social = user.social_auth.get(provider="vk-oauth2")
        api = vk.API(access_token=social.extra_data["access_token"], v=version_vk_api)
        json_vk = api.users.get(fields="photo_200")
        user.url_photo_by_user_from_VK = json_vk[0]["photo_200"]
        user.save()


class ServiceUpdatePassword(Service):
    password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
    user = ModelChoiceField(queryset=User.objects.all())

    def process(self):
        password = self.cleaned_data["password"]
        new_password = self.cleaned_data["new_password"]
        new_password2 = self.cleaned_data["new_password2"]
        user = self.cleaned_data["user"]
        self.check_password(password, new_password, new_password2, user)

    def check_password(self, password, new_password, new_password2, user):
        if check_password(password, user.password):
            if new_password != new_password2:
                raise ValueError("Новые пароли не сходятся.")
            else:
                self.changing_the_password(user, new_password)
        else:
            raise ValidationError("Ввели не верный основной пароль.")

    def changing_the_password(self, user, new_password):
        user.set_password(new_password)
        user.save()
