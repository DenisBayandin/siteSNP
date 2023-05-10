from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestGetListPhoto(APITestCase):
    def setUp(self):
        print("Create new user in TestGetListPhoto.")
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
        print("Create new token in TestGetListPhoto.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestGetListPhoto.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

        print("Create first user in TestGetListPhoto.")
        self.user_two = User.objects.create(
            username="Kinloyns",
            first_name="Denis",
            last_name="Bayandin",
            patronymic="Valerevich",
            email="email@mail.ru",
            photo_by_user=file,
        )
        self.user_two.set_password("Qaz789123")
        self.user_two.save()
        print("Create first token in TestGetListPhoto.")
        self.token_two = Token.objects.create(user_id=self.user_two.id)
        print("Create first photo in TestGetListPhoto.")
        self.photo_two = Photo.objects.create(
            name="Two photo", content="Two photo :)", old_photo=file, user=self.user_two
        )
        self.photo.go_state_on_check()
        self.photo.go_state_verified()
        self.photo.save()

        self.photo_two.go_state_on_check()
        self.photo_two.go_state_verified()
        self.photo_two.save()

    def test_get_list_photo(self):
        print("Run test_get_list_photo.")
        response = self.client.get("/api/photos/")
        self.assertEquals(response.status_code, 200)
