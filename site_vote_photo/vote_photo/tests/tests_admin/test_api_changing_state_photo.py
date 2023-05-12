from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestChangeStatePhotoAdmin(APITestCase):
    def setUp(self):
        print("Create new user in TestChangeStatePhotoAdmin.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        self.user = User.objects.create(
            username="Den4ikys",
            first_name="Denis",
            last_name="Bayandin",
            patronymic="Valerevich",
            email="email@mail.ru",
            photo_by_user=file,
            is_staff=True,
        )
        self.user.set_password("Qaz789123")
        self.user.save()
        print("Create new token in TestChangeStatePhotoAdmin.")
        self.token = Token.objects.create(user_id=self.user.id)
        print("Create new photo in TestChangeStatePhotoAdmin.")
        self.photo = Photo.objects.create(
            name="One photo", content="One photo :)", old_photo=file, user=self.user
        )

    def test_change_state_photo(self):
        print("Run test_change_state_photo.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            f"/api/admin/photo/{self.photo.id}/changing_state/on_check"
        )
        self.photo = Photo.objects.get(id=self.photo.id)
        self.assertEquals(response.status_code, 200)

    def test_change_state_photo_not_staff_user(self):
        print("Run test_change_state_photo_not_staff_user.")
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
            f"/api/admin/photo/{self.photo.id}/changing_state/on_check"
        )
        self.assertEquals(response.status_code, 403)

    def test_change_state_photo_not_valided_state(self):
        print("Run test_change_state_photo_not_valided_state.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            f"/api/admin/photo/{self.photo.id}/changing_state/asddsaasd"
        )
        self.assertEquals(response.status_code, 404)

    def test_change_state_photo_the_same_condition(self):
        print("Run test_change_state_photo_the_same_condition.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            f"/api/admin/photo/{self.photo.id}/changing_state/not_verified"
        )
        self.assertEquals(response.status_code, 400)

    def test_change_state_photo_error_404(self):
        print("Run test_change_state_photo_error_404.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(f"/api/admin/photo/500/changing_state/on_check")
        self.photo = Photo.objects.get(id=self.photo.id)
        self.assertEquals(response.status_code, 404)
