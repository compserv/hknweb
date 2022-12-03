from django.test import TestCase

from django.urls import reverse
from django.contrib.messages import get_messages

from hknweb.events.models import Rsvp

from tests.events.views.rsvp_transactions.utils import setUp


class UnrsvpViewTests(TestCase):
    def setUp(self):
        setUp(self, ["add_rsvp", "delete_rsvp"])

    def test_not_post_returns_http404(self):
        kwargs = {
            "id": 0,
        }
        response = self.client.get(reverse("events:unrsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 404)

    def test_event_doesnt_exist_returns_http404(self):
        kwargs = {
            "id": self.event.id + 1,
        }
        response = self.client.post(reverse("events:unrsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 404)

    def test_rsvp_doesnt_exist_returns_http404(self):
        kwargs = {
            "id": self.event.id,
        }
        response = self.client.post(reverse("events:unrsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 404)

    def test_rsvp_confirmed_returns_error_message(self):
        kwargs = {
            "id": self.event.id,
        }
        self.client.post(reverse("events:rsvp", kwargs=kwargs))

        rsvp = Rsvp.objects.first()
        self.assertTrue(rsvp)

        rsvp.confirmed = True
        rsvp.save()

        kwargs = {
            "id": self.event.id,
        }
        response = self.client.post(reverse("events:unrsvp", kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Cannot un-rsvp from event you have gone to."
        )

    def test_unrsvp_deletes_rsvp(self):
        kwargs = {
            "id": self.event.id,
        }
        self.client.post(reverse("events:rsvp", kwargs=kwargs))
        response = self.client.post(reverse("events:unrsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(Rsvp.objects.all(), [])
