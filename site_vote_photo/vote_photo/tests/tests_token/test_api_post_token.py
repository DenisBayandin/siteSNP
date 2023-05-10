from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestRefreshToken(APITestCase):
    def setUp(self):
        print("Create new user in TestRefreshToken.")
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
        print("Create new token in TestRefreshToken.")
        self.token = Token.objects.create(user_id=self.user.id)

    def test_refresh_token_is_available_token(self):
        print("Run test_refresh_token_is_available_token.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            "/api/token/", {"username": "Den4ikys", "password": "Qaz789123"}
        )
        print(response.data)
        self.assertEquals(response.status_code, 200)

    def test_refresh_token_is_not_available_token(self):
        print("Run test_refresh_token_is_not_available_token.")
        response = self.client.post(
            "/api/token/", {"username": "Den4ikys", "password": "Qaz789123"}
        )
        self.assertEquals(response.status_code, 401)

    def test_refresh_token_is_available_token_and_not_valided_username(self):
        print("Run test_refresh_token_is_available_token_and_not_valided_username.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            "/api/token/", {"username": "Den", "password": "Qaz789123"}
        )
        self.assertEquals(response.status_code, 404)

    def test_refresh_token_is_available_token_and_not_valided_password(self):
        print("Run test_refresh_token_is_available_token_and_not_valided_password.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            "/api/token/", {"username": "Den4ikys", "password": "Qaz"}
        )
        self.assertEquals(response.status_code, 400)

    def test_refresh_token_is_available_token_and_another_user_post_token(self):
        print("Run test_refresh_token_is_available_token_and_another_user_post_token.")
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
        user.set_password("Zcx230104")
        user.save()
        token = Token.objects.create(user_id=user.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            "/api/token/", {"username": "Den4ikys", "password": "Qaz789123"}
        )
        self.assertEquals(response.status_code, 400)
