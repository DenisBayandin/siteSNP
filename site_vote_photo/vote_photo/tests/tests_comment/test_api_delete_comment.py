from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestDeleteComment(APITestCase):
    def setUp(self):
        print("Create new user in TestDeleteComment.")
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
        print("Create new token in TestDeleteComment.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestDeleteComment.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )
        print("Create new comment in TestDeleteComment.")
        self.comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )
        print("Create first comment in TestDeleteComment.")
        self.two_comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )

    def test_delete_comment_is_available_token(self):
        print("Run test_delete_comment_is_available_token.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/api/comments/{self.comment.id}")
        self.assertEquals(response.status_code, 204)

    def test_delete_comment_is_not_available_token(self):
        print("Run test_delete_comment_is_not_available_token.")
        response = self.client.delete(f"/api/comments/{self.comment.id}")
        self.assertEquals(response.status_code, 401)

    def test_delete_another_user_delete_comment(self):
        print("Run test_delete_another_user_delete_comment.")
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
        response = self.client.delete(f"/api/comments/{self.comment.id}")
        self.comment.refresh_from_db()
        self.assertEquals(response.status_code, 400)

    def test_delete_comment_with_parent(self):
        print("Run test_delete_comment_with_parent.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.two_comment.parent = self.comment
        self.two_comment.save()
        self.two_comment.refresh_from_db()
        response = self.client.delete(f"/api/comments/{self.comment.id}")
        self.assertEquals(response.status_code, 400)

    def test_delete_comment_is_not_valided_url(self):
        print("Run test_delete_comment_is_not_valided_url.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/api/comments/500")
        self.assertEquals(response.status_code, 404)
