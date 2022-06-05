from django.test import TestCase

from django.urls import reverse


class LandingViewsTests(TestCase):
    def test_landing_get_returns_200(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_about_get_returns_200(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
