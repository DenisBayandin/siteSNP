from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestGetToken(APITestCase):
    def setUp(self):
        print("Create new user in TestGetToken.")
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
        print("Create new token in TestGetToken.")
        self.token = Token.objects.create(user_id=self.user.id)

    def test_get_token(self):
        print("Run test_get_token.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/auth/token")
        self.assertEquals(response.status_code, 200)

    def test_get_token_not_auth(self):
        print("Run test_get_token_not_auth.")
        response = self.client.get("/api/auth/token")
        self.assertEquals(response.status_code, 400)
