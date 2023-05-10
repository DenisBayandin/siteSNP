from rest_framework.test import APITestCase
from django.core.files import File
from rest_framework.authtoken.models import Token
from vote_photo.models import *


class TestChangeStatePhotoAdmin(APITestCase):
    def setUp(self):
        print("Create new user in TestChangeStatePhotoAdmin.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        open_file_two = open("vote_photo/tests/gangsta.jpg", "rb")
        file_two = File(open_file_two)
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
            name="One photo",
            content="One photo :)",
            old_photo=file,
            new_photo=file_two,
            user=self.user,
            state="Update",
        )

    def test_update_photo(self):
        print("Run test_update_photo.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.put(
            f"/api/admin/photo/{self.photo.id}/apply_change_photo"
        )
        self.photo = Photo.objects.get(id=self.photo.id)
        self.assertEquals(response.status_code, 200)

    def test_update_photo_not_state_update(self):
        print("Run test_update_photo_not_state_update.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.photo.go_state_not_verified()
        self.photo.save()
        self.photo = Photo.objects.get(id=self.photo.id)
        response = self.client.put(
            f"/api/admin/photo/{self.photo.id}/apply_change_photo"
        )
        self.assertEquals(response.status_code, 400)

    def test_update_photo_error_404(self):
        print("Run test_update_photo_error_404.")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.put(f"/api/admin/photo/500/apply_change_photo")
        self.photo = Photo.objects.get(id=self.photo.id)
        self.assertEquals(response.status_code, 404)

    def test_update_photo_user_not_staff(self):
        print("Run test_update_photo_user_not_staff.")
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

        response = self.client.put(
            f"/api/admin/photo/{self.photo.id}/apply_change_photo"
        )
        self.photo = Photo.objects.get(id=self.photo.id)
        self.assertEquals(response.status_code, 403)
