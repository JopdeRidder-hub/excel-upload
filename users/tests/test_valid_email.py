from django.test import TestCase

from users.utils import _is_valid_email


class ValidEmailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.wrong_email = "not_valid_email"
        cls.wrong_email_2 = "not_valid_email.com"
        cls.valid_email = "test@test.com"

    def test_valid_email(self):
        self.assertFalse(_is_valid_email(self.wrong_email))
        self.assertFalse(_is_valid_email(self.wrong_email_2))
        self.assertTrue(_is_valid_email(self.valid_email))
