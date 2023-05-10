from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestFilterPhoto(APITestCase):
    def setUp(self):
        print("Create new user in TestFilterPhoto.")
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
        print("Create new token in TestFilterPhoto.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestFilterPhoto.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

    def test_get_photo_with_filter(self):
        print("Run test_get_photo_with_filter.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/photos/not_verified/")
        self.assertEquals(response.status_code, 200)

    def test_get_photo_with_filter_invalid_filter(self):
        print("Run test_get_photo_with_filter_invalid_filter.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/photos/afdsfs/")
        print(f"\nresponse data with invalid filter = {response.data}")
        self.assertEquals(response.status_code, 404)

    def test_get_photo_with_filter_is_not_available_token(self):
        print("Run test_get_photo_with_filter_is_not_available_token.")
        response = self.client.get("/api/photos/not_verified/")
        self.assertEquals(response.status_code, 401)
