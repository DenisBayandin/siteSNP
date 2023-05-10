from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestGetListLike(APITestCase):
    def setUp(self):
        print("Create new user in TestGetListLike.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        self.user = User.objects.create(
            username="Den4ikys",
            first_name="Denis",
            last_name="Bayandin",
            patronymic="Valerevich",
            email="email@mail.ru",
            photo_by_user=file,
        )
        self.user.set_password("Qaz789123")
        self.user.save()
        print("Create new token in TestGetListLike.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestGetListLike.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

    def test_get_list_like(self):
        print("Run test_get_list_like.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        user = User.objects.create(
            username="Kinloyns",
            first_name="Denis",
            last_name="Bayandin",
            patronymic="Valerevich",
            email="email@mail.ru",
            photo_by_user=file,
        )
        Like.objects.create(
            user=self.user,
            photo=self.photo,
        )
        Like.objects.create(
            user=user,
            photo=self.photo,
        )
        response = self.client.get(f"/api/likes/{self.photo.id}/")
        self.assertEquals(response.status_code, 200)
