from django.test import TestCase

from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse("tutoring:index"))

        self.assertEqual(response.status_code, 200)
