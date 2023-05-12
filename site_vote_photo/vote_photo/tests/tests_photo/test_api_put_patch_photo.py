from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestPutPatchPhoto(APITestCase):
    def setUp(self):
        print("Create new user in TestPutPatchPhoto.")
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
        print("Create new token in TestPutPatchPhoto.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestPutPatchPhoto.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

    def open_to_update_photo(self):
        print("Run open_to_update_photo.")
        open_file = open("vote_photo/tests/gangsta.jpg", "rb")
        file = File(open_file)
        return file

    def test_put_photo_is_available_token(self):
        print("Run test_put_photo_is_available_token.")
        file = self.open_to_update_photo()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.put(
            f"/api/photos/{self.photo.id}",
            {
                "name": "Update photo",
                "content": "Updateeee...",
                "new_photo": file,
            },
        )
        self.assertEquals(response.status_code, 200)

    def test_put_photo_is_not_available_token(self):
        print("Run test_put_photo_is_not_available_token.")
        file = self.open_to_update_photo()
        response = self.client.put(
            f"/api/photos/{self.photo.id}",
            {
                "name": "Update photo",
                "content": "Updateeee...",
                "new_photo": file,
            },
        )
        self.assertEquals(response.status_code, 401)

    def test_put_photo_is_available_token_is_update_another_user(self):
        print("Run test_put_photo_is_available_token_is_update_another_user.")
        file = self.open_to_update_photo()
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
        response = self.client.put(
            f"/api/photos/{self.photo.id}",
            {
                "name": "Update photo",
                "content": "Updateeee...",
                "new_photo": file,
            },
        )
        self.assertEquals(response.status_code, 400)

    def test_put_photo_is_available_token_not_valided_url(self):
        print("Run test_put_photo_is_available_token_not_valided_url.")
        file = self.open_to_update_photo()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.put(
            f"/api/photos/500",
            {
                "name": "Update photo",
                "content": "Updateeee...",
                "new_photo": file,
            },
        )
        self.assertEquals(response.status_code, 404)
