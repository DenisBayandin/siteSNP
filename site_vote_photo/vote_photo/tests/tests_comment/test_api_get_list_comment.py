from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestGetListComment(APITestCase):
    def setUp(self):
        print("Create new user in TestGetListComment.")
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
        print("Create new token in TestGetListComment.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestGetListComment.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )
        print("Create new comment in TestGetListComment.")
        self.comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )
        print("Create first comment in TestGetListComment.")

        self.two_comment = Comment.objects.create(
            content="123", user=self.user, photo=self.photo
        )

    def test_get_list_comment_is_valided_url(self):
        print("Run test_get_list_comment_is_valided_url.")
        response = self.client.get(f"/api/comments/photo/{self.photo.id}")
        self.assertEquals(response.status_code, 200)

    def test_get_list_comment_is_not_valided_url(self):
        print("Run test_get_list_comment_is_not_valided_url.")
        response = self.client.get("/api/comments/photo/500")
        self.assertEquals(response.status_code, 404)
