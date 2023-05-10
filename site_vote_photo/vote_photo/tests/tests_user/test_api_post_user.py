from django.core.files import File
from django.test import TestCase


class TestCreateUser(TestCase):
    def test_create_user_post_request(self):
        print("Run test_create_user_post_request.")
        open_file = open("vote_photo/tests/profile_admin.jpg", "rb")
        file = File(open_file)
        user_data = {
            "username": "Den4ikys",
            "first_name": "Denis",
            "last_name": "Bayandin",
            "patronymic": "Valerevich",
            "email": "email@mail.ru",
            "name": "fred",
            "photo_by_user": file,
            "password": "Qaz789123",
            "password2": "Qaz789123",
        }
        response = self.client.post("/api/users/", data=user_data, follow=True)
        self.assertEquals(response.status_code, 200)
