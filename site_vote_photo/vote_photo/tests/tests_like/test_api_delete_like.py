from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestDeleteLike(APITestCase):
    def setUp(self):
        print("Create new user in TestDeleteLike.")
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
        print("Create new token in TestDeleteLike.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestDeleteLike.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

    def test_delete_like_is_available_token(self):
        print("Run test_delete_like_is_available_token.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        Like.objects.create(
            user=self.user,
            photo=self.photo,
        )
        response = self.client.delete(f"/api/likes/{self.photo.id}")
        self.assertEquals(response.status_code, 204)

    def test_delete_like_is_available_token_not_valided_url_not_found_photo(self):
        print(
            "Run test_delete_like_is_available_token_not_valided_url_not_found_photo."
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        Like.objects.create(
            user=self.user,
            photo=self.photo,
        )
        response = self.client.delete(f"/api/likes/500")
        self.assertEquals(response.status_code, 404)

    def test_delete_like_valided_data_is_not_available_token(self):
        print("Run test_delete_like_valided_data_is_not_available_token.")
        Like.objects.create(
            user=self.user,
            photo=self.photo,
        )
        response = self.client.delete(f"/api/likes/{self.photo.id}")
        self.assertEquals(response.status_code, 401)

    def test_delete_like_not_have_like_photo(self):
        print("Run test_delete_like_not_have_like_photo.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/api/likes/{self.photo.id}")
        self.assertEquals(response.status_code, 404)
