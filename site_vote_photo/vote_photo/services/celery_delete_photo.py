from channels.layers import get_channel_layer
from service_objects.services import Service
from django.utils import timezone

from ..models import *


channel_layer = get_channel_layer()


class ServiceCeleryDeletePhoto(Service):
    def process(self):
        self.check_the_time_and_delete(Photo.objects.filter(state="Delete"))
        return self.what_to_return_to_the_main_function(
            Photo.objects.filter(state="Delete").count()
        )

    def check_the_time_and_delete(self, queryset_photo):
        for one_photo_delete in queryset_photo:
            if timezone.now() >= one_photo_delete.date_delete:
                one_photo_delete.delete()

    def what_to_return_to_the_main_function(self, count_photo):
        if count_photo >= 1:
            return "There are photos to delete."
        else:
            return "No photos to delete."
