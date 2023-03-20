from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from django.contrib.auth import logout


def rename_lifetime_token_vk(request, user):
    if user.photo_by_user.name == "":
        social = user.social_auth.get(provider="vk-oauth2")
        time_life_token = social.extra_data["expires"]
        if social.created + timedelta(seconds=time_life_token) < timezone.now():
            social.created = social.modified
            social.save()
            logout(request)
            return True
