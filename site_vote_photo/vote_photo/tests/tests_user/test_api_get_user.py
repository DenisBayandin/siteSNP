from django.test import TestCase
from vote_photo.models import *


class TestGetUsers(TestCase):
    def setUp(self):
        print("Create new user in TestGetUsers.")
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

    def test_get_user(self):
        print("Run test_get_user.")
        response = self.client.get("/api/users/")
        self.assertEquals(response.status_code, 200)
