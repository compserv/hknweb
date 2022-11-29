from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages

from tests.events.views.event_transactions.utils import setUp


class ShowEventViewTests(TestCase):
    def setUp(self):
        setUp(self, "view_event")

    def test_event_doesnt_exist_returns_404(self):
        kwargs = {
            "id": self.event.id + 1,
        }
        response = self.client.get(reverse("events:detail", kwargs=kwargs))

        self.assertEqual(response.status_code, 404)

    def test_insufficient_access_level_redirects_with_error_message(self):
        kwargs = {
            "id": self.event.id,
        }
        response = self.client.get(reverse("events:detail", kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Insufficent permission to access event.")

    def test_returns_200(self):
        group = Group(name="officer")
        group.save()
        group.user_set.add(self.user)
        group.save()

        kwargs = {
            "id": self.event.id,
        }
        response = self.client.get(reverse("events:detail", kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
