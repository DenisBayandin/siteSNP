from service_objects.services import Service
from service_objects.fields import ModelField
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img

import io

from vote_photo.models import *


class NewSizePhotoService(Service):
    photo = ModelField(Photo)

    def process(self):
        self.new_photo_size_510_510(self.cleaned_data["photo"])
        self.new_photo_size_145_165(self.cleaned_data["photo"])
        self.cleaned_data["photo"].save()

    def new_photo_size_510_510(self, photo):
        byteImgIO = io.BytesIO()
        byteImg = Img.open(photo.old_photo)
        byteImg.thumbnail((510, 510), Img.ANTIALIAS)
        byteImg.save(byteImgIO, format="JPEG", quality=90)
        byteImgIO.seek(0)
        photo.photo_510x510 = InMemoryUploadedFile(
            byteImgIO,
            "ImageField",
            photo.old_photo.name,
            "image/jpeg",
            byteImgIO.__sizeof__(),
            None,
        )

    def new_photo_size_145_165(self, photo):
        byteImgIO_two = io.BytesIO()
        byteImg_two = Img.open(photo.old_photo)
        byteImg_two.thumbnail((145, 165), Img.ANTIALIAS)
        byteImg_two.save(byteImgIO_two, format="JPEG", quality=90)
        byteImgIO_two.seek(0)
        photo.photo_145x165 = InMemoryUploadedFile(
            byteImgIO_two,
            "ImageField",
            photo.old_photo.name,
            "image/jpeg",
            byteImgIO_two.__sizeof__(),
            None,
        )
