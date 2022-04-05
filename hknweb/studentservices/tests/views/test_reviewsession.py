from django.test import TestCase

from django.urls import reverse

from hknweb.events.models import EventType
from hknweb.events.tests.models.utils import ModelFactory


class ReviewSessionViewTests(TestCase):
    def test_reviewsessions_get(self):
        response = self.client.get(reverse("studentservices:reviewsessions"))

        self.assertEqual(response.status_code, 200)

    def test_reviewsessions_details(self):
        user = ModelFactory.create_user()
        event_type = EventType.objects.create(type="Review Session")
        rs = ModelFactory.create_event(
            name="custom event name",
            event_type=event_type,
            created_by=user,
            access_level=2,
        )

        kwargs = {"id": rs.id}
        response = self.client.get(reverse("studentservices:show_reviewsession_details", kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
