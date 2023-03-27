from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist


def rename_lifetime_token_vk(request, user):
    try:
        if user.photo_by_user.name == "":
            social = user.social_auth.get(provider="vk-oauth2")
            if (
                social.created + timedelta(seconds=social.extra_data["expires"])
                < timezone.now()
            ):
                social.created = social.modified
                social.save()
                logout(request)
                return True
    except ObjectDoesNotExist:
        return False
