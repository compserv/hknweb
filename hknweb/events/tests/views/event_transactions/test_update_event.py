from django.test import TestCase

from django.urls import reverse

from hknweb.events.tests.views.event_transactions.utils import setUp


class UpdateEventViewTests(TestCase):
    def setUp(self):
        setUp(self, "change_event")

    def test_returns_200(self):
        kwargs = {
            "pk": self.event.id,
        }
        response = self.client.get(reverse("events:edit", kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
