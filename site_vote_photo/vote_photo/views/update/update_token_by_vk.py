from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from vote_photo.services.updatedata.update_token_by_VK import (
    ServiceRenameLifetimeTokenVk,
)


def rename_lifetime_token_vk(request, user):
    try:
        if ServiceRenameLifetimeTokenVk.execute({"user": user}):
            logout(request)
            return True
    except ObjectDoesNotExist:
        return False
