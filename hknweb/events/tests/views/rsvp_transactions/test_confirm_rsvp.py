from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from hknweb.events.models import Rsvp

from hknweb.events.tests.models.utils import ModelFactory


class RsvpViewTests(TestCase):
    def setUp(self):
        user = ModelFactory.create_user()
        password = "custom password"
        user.set_password(password)
        user.save()

        content_type = ContentType.objects.get_for_model(Rsvp)
        permission = Permission.objects.get(content_type=content_type, codename="add_rsvp")
        user.user_permissions.add(permission)

        self.client.login(username=user.username, password=password)

        event_type = ModelFactory.create_event_type()
        event = ModelFactory.create_event(
            name="custom event name",
            event_type=event_type,
            created_by=user,
            access_level=2,
        )

        kwargs = {
            "id": event.id,
        }
        self.client.post(reverse("events:rsvp", kwargs=kwargs))

        rsvp = Rsvp.objects.first()

        self.user = user
        self.password = password
        self.event = event
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
