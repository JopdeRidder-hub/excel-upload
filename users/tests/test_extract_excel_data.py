from django.test import TestCase

from users.utils import (
    create_users_from_excel_file,
    extract_excel_data,
)
from users.models import User
import os


class ExtractExcelDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.valid_excel_file = "valid_sheet.xlsx"
        cls.invalid_file = "invalid_sheet.xlsx"
        cls.invalid_email_file = "invalid_email_sheet.xlsx"

    def test_extract_excel_data(self):

        file = fixture_path(self.valid_excel_file)
        data = extract_excel_data(file)

        expected_data = [
            ["email", "first_name", "last_name", "team"],
            ["test@test.com", "test", "last1", "Team1"],
            ["test2@test.com", "test2", "last2", "Team2"],
            ["test3@test.com", "test3", "last3", "Team3"],
        ]

        self.assertEqual(data, expected_data)

    def test_create_users_from_excel_file(self):
        file = fixture_path(self.valid_excel_file)
        data, error = create_users_from_excel_file(file)

        expected_data = [
            [
                "3 new user(s) are created",
                "0 user(s) where already present",
                "0 invalid email(s)",
            ],
            ["email", "first_name", "last_name", "team"],
            ["test@test.com", "test", "last1", "Team1", "user created"],
            ["test2@test.com", "test2", "last2", "Team2", "user created"],
            ["test3@test.com", "test3", "last3", "Team3", "user created"],
        ]

        self.assertEqual(data, expected_data)
        self.assertIsNone(error)

    def test_create_users_already_exist(self):
        file = fixture_path(self.valid_excel_file)

        User.objects.create(email="test@test.com", username="testlast1")

        data, error = create_users_from_excel_file(file)

        expected_data = [
            [
                "2 new user(s) are created",
                "1 user(s) where already present",
                "0 invalid email(s)",
            ],
            ["email", "first_name", "last_name", "team"],
            ["test@test.com", "test", "last1", "Team1", "user already exists"],
            ["test2@test.com", "test2", "last2", "Team2", "user created"],
            ["test3@test.com", "test3", "last3", "Team3", "user created"],
        ]

        self.assertEqual(data, expected_data)
        self.assertIsNone(error)

    def test_create_users_invalid_email(self):
        file = fixture_path(self.invalid_file)

        data, error = create_users_from_excel_file(file)

        self.assertEqual(
            error,
            "Please make sure to use the right header order: | email | first_name | last_name | team |",
        )
        self.assertIsNone(data)

    def test_create_users_invalid_email(self):
        file = fixture_path(self.invalid_email_file)

        data, error = create_users_from_excel_file(file)
        expected_data = [
            [
                "2 new user(s) are created",
                "0 user(s) where already present",
                "1 invalid email(s)",
            ],
            ["email", "first_name", "last_name", "team"],
            ["test@test.com", "test", "last1", "Team1", "user created"],
            ["test2@test.com", "test2", "last2", "Team2", "user created"],
            ["test3test.com", "test3", "last3", "Team3", "not a correct email"],
        ]

        self.assertEqual(data, expected_data)
        self.assertIsNone(error)


def fixture_path(filename):
    return os.path.join(os.path.dirname(__file__), "fixtures", filename)
