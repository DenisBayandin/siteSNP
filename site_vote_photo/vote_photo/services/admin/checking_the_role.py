from django.http import Http404
from service_objects.fields import ModelField
from rest_framework import status

from vote_photo.models import *
from ...utils.services.custom_service import ServiceWithResult


class CheckRoleUserService(ServiceWithResult):
    user = ModelField(User)

    custom_validations = ["check_role"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            return self
        raise Http404("No rights.")

    def check_role(self):
        if not (
            self.cleaned_data["user"].is_superuser
            and self.cleaned_data["user"].is_staff
        ):
            self.add_error(
                "id",
                f"The user does not have the right to perform this function.",
            )
            self.response_status = status.HTTP_404_NOT_FOUND
