from rest_framework.test import APITestCase
from django.urls import reverse
import os

from users.models import User


class TestUserAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.wrong_file_type = "wrong_file_type.jpg"
        cls.valid_file_type = "valid_sheet.xlsx"
        cls.url = reverse("user-excel-upload")
        cls.user = User.objects.create(username="user", is_superuser=True)

    def test_api_wrong_file_type(self):
        file = fixture_path(self.wrong_file_type)
        self.client.force_authenticate(user=self.user)
        with open(file, "rb") as read_file:
            response = self.client.post(self.url, {"file": read_file})

        expected_data = {
            "excel_data": [],
            "error": "wrong_file_type.jpg not allowed, please upload an excel file",
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    def test_api_valid_file_type(self):
        file = fixture_path(self.valid_file_type)
        self.client.force_authenticate(user=self.user)
        with open(file, "rb") as read_file:
            response = self.client.post(self.url, {"file": read_file})

        excepted_data = {
            "excel_data": [
                [
                    "3 new user(s) are created",
                    "0 user(s) where already present",
                    "0 invalid email(s)",
                ],
                ["email", "first_name", "last_name", "team"],
                ["test@test.com", "test", "last1", "Team1", "user created"],
                ["test2@test.com", "test2", "last2", "Team2", "user created"],
                ["test3@test.com", "test3", "last3", "Team3", "user created"],
            ],
            "error": None,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, excepted_data)

    def test_api_valid_file_type(self):
        file = fixture_path(self.valid_file_type)

        with open(file, "rb") as read_file:
            response = self.client.post(self.url, {"file": read_file})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "not_authenticated")


def fixture_path(filename):
    return os.path.join(os.path.dirname(__file__), "fixtures", filename)
