from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages

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
        permission = Permission.objects.get(content_type=content_type, codename="delete_rsvp")
        user.user_permissions.add(permission)

        self.client.login(username=user.username, password=password)

        event_type = ModelFactory.create_event_type()
        event = ModelFactory.create_event(
            name="custom event name",
            event_type=event_type,
            created_by=user,
            access_level=2,
        )

        self.user = user
        self.password = password
        self.event = event

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
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Cannot un-rsvp from event you have gone to.")

    def test_unrsvp_deletes_rsvp(self):
        kwargs = {
            "id": self.event.id,
        }
        self.client.post(reverse("events:rsvp", kwargs=kwargs))
        response = self.client.post(reverse("events:unrsvp", kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(Rsvp.objects.all(), [])
