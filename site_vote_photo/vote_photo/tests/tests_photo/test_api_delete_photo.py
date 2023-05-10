from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestDeletePhoto(APITestCase):
    def setUp(self):
        print("Create new user in TestDeletePhoto.")
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
        print("Create new token in TestDeletePhoto.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestDeletePhoto.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

    def test_delete_photo_is_available_token(self):
        print("Run test_delete_photo_is_available_token.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/api/photos/{self.photo.id}/")
        self.assertEquals(response.status_code, 204)

    def test_delete_photo_is_not_available_token(self):
        print("Run test_delete_photo_is_not_available_token.")
        response = self.client.delete(f"/api/photos/{self.photo.id}/")
        self.assertEquals(response.status_code, 401)

    def test_delete_photo_is_available_token_delete_another_user(self):
        print("Run test_delete_photo_is_available_token_delete_another_user.")
        open_file = open("vote_photo/tests/gangsta.jpg", "rb")
        file = File(open_file)
        user = User.objects.create(
            username="Kinloyns",
            first_name="Denis",
            last_name="Bayandin",
            patronymic="Valerevich",
            email="email@mail.ru",
            photo_by_user=file,
        )
        user.set_password("Qaz789123")
        user.save()
        token = Token.objects.create(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.delete(f"/api/photos/{self.photo.id}/")
        self.assertEquals(response.status_code, 400)

    def test_delete_photo_is_available_token_is_error_404(self):
        print("Run test_delete_photo_is_available_token_is_error_404.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/api/photos/500/")
        self.assertEquals(response.status_code, 404)
