from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestRetrieveComment(APITestCase):
    def setUp(self):
        print("Create new user in TestRetrieveComment.")
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
        print("Create new token in TestRetrieveComment.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestRetrieveComment.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )
        print("Create new comment in TestRetrieveComment.")
        self.comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )

    def test_retrieve_comment_is_available_token(self):
        print("Run test_retrieve_comment_is_available_token.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(f"/api/comments/{self.comment.id}/")
        print(response.data)
        self.assertEquals(response.status_code, 200)

    def test_retrieve_comment_is_not_available_token(self):
        print("Run test_retrieve_comment_is_not_available_token.")
        response = self.client.get(f"/api/comments/{self.comment.id}/")
        self.assertEquals(response.status_code, 401)

    def test_retrieve_comment_is_available_token_not_valided_url(self):
        print("Run test_retrieve_comment_is_available_token_not_valided_url.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(f"/api/comments/500/")
        self.assertEquals(response.status_code, 404)
