from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from hknweb.utils import DATETIME_12_HOUR_FORMAT


class ToursViewTests(TestCase):
    def test_tours_get(self):
        response = self.client.get(reverse("studentservices:tours"))

        self.assertEqual(response.status_code, 200)

    def test_tours_form_valid_redirects(self):
        data = {
            "name": "test_name",
            "datetime": timezone.now().strftime(DATETIME_12_HOUR_FORMAT),
            "email": "test_email@email.com",
            "phone": "9876543210",
            "comments": "test_comments",
        }
        response = self.client.post(reverse("studentservices:tours"), data=data)

        self.assertEqual(response.status_code, 302)

    def test_tours_form_invalid_returns_form(self):
        data = {
            "name": "test_name",
            "datetime": timezone.now().strftime(DATETIME_12_HOUR_FORMAT),
            "email": "test_email",
            "phone": "9876543210",
            "comments": "test_comments",
        }
        response = self.client.post(reverse("studentservices:tours"), data=data)

        self.assertEqual(response.status_code, 200)

    def test_tours_form_datetime_invalid_returns_form(self):
        data = {
            "name": "test_name",
            "datetime": (timezone.now() - timezone.timedelta(days=20)).strftime(DATETIME_12_HOUR_FORMAT),
            "email": "test_email@email.com",
            "phone": "9876543210",
            "comments": "test_comments",
        }
        response = self.client.post(reverse("studentservices:tours"), data=data)

        self.assertEqual(response.status_code, 200)
