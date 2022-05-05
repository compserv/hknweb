from django.conf import settings
from django.test import TestCase

from django.urls import reverse

from hknweb.events.tests.models.utils import ModelFactory


class UsersViewsTests(TestCase):
    def setUp(self):
        password = "custom password"
        user = ModelFactory.create_user(
            username="test_user",
            email="test_user@berkeley.edu",
        )
        user.set_password(password)
        user.save()

        self.user = user
        self.password = password

    def test_account_settings_get_returns_200(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse("account-settings"))

        self.assertEqual(response.status_code, 200)

    def test_account_settings_verify_form_invalid_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {}
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_settings_incorrect_current_password_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            "password": "incorrect_password",
        }
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_settings_invalid_password_form_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            "password": self.password,
            "change_password": True,
        }
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_settings_valid_password_form_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            "password": self.password,
            "change_password": True,
            "new_password1": "test_new_password",
            "new_password2": "test_new_password",
        }
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_settings_invalid_profile_form_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            "password": self.password,
            "edit_profile": True,
            "phone_number": "incorrect_phone_number",
        }
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_settings_valid_profile_form_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            "password": self.password,
            "edit_profile": True,
            "phone_number": "1234567890",
        }
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_settings_missing_action_returns_302(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            "password": self.password,
            "incorrect_action_name": True,
        }
        response = self.client.post(reverse("account-settings"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_account_create_get_returns_200(self):
        response = self.client.get(reverse("account-create"))

        self.assertEqual(response.status_code, 200)

    def test_account_create_returns_302(self):
        settings.DEBUG = True

        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "username": "test_username",
            "email": "test_email@berkeley.edu",
            "password1": "test_password",
            "password2": "test_password",
        }
        response = self.client.post(reverse("account-create"), data=data)

        self.assertEqual(response.status_code, 302)

        settings.DEBUG = False
