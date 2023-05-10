from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestPutPatchUser(APITestCase):
    def setUp(self):
        print("Create new user in TestPutPatchUser.")
        self.user = User.objects.create(
            username="Den4ikys",
            first_name="Denis",
            last_name="Bayandin",
            patronymic="Valerevich",
            email="email@mail.ru",
            photo_by_user=None,
        )
        self.user.set_password("Qaz789123")
        self.user.save()
        print("Create new token in TestPutPatchUser.")
        self.token = Token.objects.create(user_id=self.user.id)

    def test_put_is_available_token_and_valided_password(self):
        print("Run test_put_is_available_token_and_valided_password.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        request = self.client.put(
            f"/api/users/{self.user.id}/",
            {
                "password": "Qaz789123",
                "new_password": "Zxc230104",
                "new_password2": "Zxc230104",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 200)

    def test_put_is_available_token_and_valided_data(self):
        print("Run test_put_is_available_token_and_valided_data.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        request = self.client.put(
            f"/api/users/{self.user.id}/",
            {
                "username": "12",
                "first_name": "34",
                "last_name": "56",
                "patronymic": "78",
                "email": "910@mail.ru",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 200)

    def test_is_available_token_not_found_user(self):
        print("Run test_is_available_token_not_found_user.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        request = self.client.put(
            "/api/users/151/",
            {
                "username": "12",
                "first_name": "34",
                "last_name": "56",
                "patronymic": "78",
                "email": "910@mail.ru",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 404)

    def test_put_is_not_available_token_and_valided_data(self):
        print("Run test_put_is_not_available_token_and_valided_data.")
        request = self.client.put(
            f"/api/users/{self.user.id}/",
            {
                "username": "12",
                "first_name": "34",
                "last_name": "56",
                "patronymic": "78",
                "email": "910@mail.ru",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 401)

    def test_put_is_available_token_request_user_id_does_not_equal_user_id(self):
        print("Run test_put_is_available_token_request_user_id_does_not_equal_user_id.")
        user = User.objects.create(username="TestUser").id
        token = Token.objects.create(user_id=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        request = self.client.put(
            f"/api/users/{self.user.id}/",
            {
                "username": "12",
                "first_name": "34",
                "last_name": "56",
                "patronymic": "78",
                "email": "910@mail.ru",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 400)

    def test_put_not_valided_password(self):
        print("Run test_put_not_valided_password.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        request = self.client.put(
            f"/api/users/{self.user.id}/",
            {
                "password": "Qaz",
                "new_password": "Zxc230104",
                "new_password2": "Zxc230104",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 400)

    def test_put_not_valided_new_password(self):
        print("Run test_put_not_valided_new_password.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        request = self.client.put(
            f"/api/users/{self.user.id}/",
            {
                "password": "Qaz789123",
                "new_password": "Zxc230104",
                "new_password2": "Zxc",
            },
        )
        self.user.refresh_from_db()
        self.assertEquals(request.status_code, 400)
