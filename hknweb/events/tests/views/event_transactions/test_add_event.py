from django.test import TestCase

from django.urls import reverse

from hknweb.events.tests.views.event_transactions.utils import setUp


class AddEventViewTests(TestCase):
    def setUp(self):
        setUp(self, "add_event")

    def test_returns_200(self):
        response = self.client.get(reverse("events:new"))

        self.assertEqual(response.status_code, 200)
