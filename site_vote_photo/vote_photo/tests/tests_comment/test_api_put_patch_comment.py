from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestPutPatchComment(APITestCase):
    def setUp(self):
        print("Create new user in TestPutPatchComment.")
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
        print("Create new token in TestPutPatchComment.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestPutPatchComment.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )
        print("Create new comment in TestPutPatchComment.")
        self.comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )
        print("Create first comment in TestPutPatchComment.")
        self.two_comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )

    def test_put_is_available_token_and_valided_data(self):
        print("Run test_put_is_available_token_and_valided_data.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.put(
            f"/api/comments/{self.comment.id}/",
            {"content": "Denis update this comment.", "parent": self.two_comment.id},
        )
        self.comment.refresh_from_db()
        self.assertEquals(response.status_code, 200)

    def test_put_is_available_token_and_not_valided_data(self):
        print("Run test_put_is_available_token_and_not_valided_data.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.put(
            f"/api/comments/{self.comment.id}/",
            {"content": "Denis update this comment.", "parent": self.two_comment},
        )
        self.comment.refresh_from_db()
        self.assertEquals(response.status_code, 400)

    def test_put_is_not_available_token_and_valided_data(self):
        print("Run test_put_is_not_available_token_and_valided_data/")
        response = self.client.put(
            f"/api/comments/{self.comment.id}/",
            {"content": "Denis update this comment.", "parent": self.two_comment.id},
        )
        self.comment.refresh_from_db()
        self.assertEquals(response.status_code, 401)

    def test_put_is_available_token_and_valided_data_and_update_another_user(self):
        print(
            "Run test_put_is_available_token_and_valided_data_and_update_another_user."
        )
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
        user.set_password("Qaz789123")
        user.save()
        token = Token.objects.create(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            f"/api/comments/{self.comment.id}/",
            {"content": "Denis update this comment.", "parent": self.two_comment.id},
        )
        self.comment.refresh_from_db()
        self.assertEquals(response.status_code, 400)
