from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestCreatePhoto(APITestCase):
    def setUp(self):
        print("Create new user in TestCreatePhoto.")
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
        print("Create new token in TestCreatePhoto.")
        self.token = Token.objects.create(user_id=self.user.id)

    def test_create_photo_and_is_available_token(self):
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            "/api/photos/",
            {
                "name": "Create photo is request post photo.",
                "content": "Create photo is request post photo.",
                "old_photo": file,
                "user": self.user.id,
            },
        )
        self.assertEquals(response.status_code, 200)

    def test_create_photo_and_is_not_available_token(self):
        print("Run test_create_photo_and_is_not_available_token.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        response = self.client.post(
            "/api/photos/",
            {
                "name": "Create photo is request post photo.",
                "content": "Create photo is request post photo.",
                "old_photo": file,
                "user": self.user.id,
            },
        )
        self.assertEquals(response.status_code, 401)

    def test_create_photo_and_is_available_token_and_not_valided_data(self):
        print("Run test_create_photo_and_is_available_token_and_not_valided_data.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            "/api/photos/",
            {
                "name": "Create photo is request post photo.",
                "content": "Create photo is request post photo.",
                "old_photo": file,
                "user": self.user,
            },
        )
        print(response.data)
        self.assertEquals(response.status_code, 400)
