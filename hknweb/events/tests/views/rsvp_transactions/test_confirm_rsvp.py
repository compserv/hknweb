from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import Group

from hknweb.events.models import Rsvp

from hknweb.events.tests.views.rsvp_transactions.utils import setUp


class ConfirmRsvpViewTests(TestCase):
    def setUp(self):
        setUp(self, ["add_rsvp"])

        kwargs = {
            "id": self.event.id,
        }
        self.client.post(reverse("events:rsvp", kwargs=kwargs))

        rsvp = Rsvp.objects.first()
        self.rsvp = rsvp

    def test_not_post_returns_http404(self):
        kwargs = {
            "id": 0,
            "operation": 0,
        }
        response = self.client.get(reverse("events:confirm_rsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 404)

    def test_access_level_gt_0_returns_403(self):
        kwargs = {
            "id": self.rsvp.id,
            "operation": 0,
        }
        response = self.client.post(reverse("events:confirm_rsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 403)

    def test_confirm_sets_confirmed(self):
        group = Group(name="officer")
        group.save()
        group.user_set.add(self.user)
        group.save()

        kwargs = {
            "id": self.rsvp.id,
            "operation": 0,
        }
        response = self.client.post(reverse("events:confirm_rsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rsvp.objects.first().confirmed)

    def test_unconfirm_sets_unconfirmed(self):
        group = Group(name="officer")
        group.save()
        group.user_set.add(self.user)
        group.save()

        kwargs = {
            "id": self.rsvp.id,
            "operation": 1,
        }
        response = self.client.post(reverse("events:confirm_rsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rsvp.objects.first().confirmed)
