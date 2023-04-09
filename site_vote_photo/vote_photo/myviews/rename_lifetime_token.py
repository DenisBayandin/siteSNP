from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from ..services.service_rename_lifetime_token_vk import ServiceRenameLifetimeTokenVk


def rename_lifetime_token_vk(request, user):
    try:
        if ServiceRenameLifetimeTokenVk.execute({"user": user}):
            logout(request)
            return True
    except ObjectDoesNotExist:
        return False
