from django.test import TestCase

from django.urls import reverse

from hknweb.events.tests.models.utils import ModelFactory


class IndexViewTests(TestCase):
    def test_no_event_types(self):
        response = self.client.get(reverse("events:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["event_types"], [])

    def test_no_events_with_event_type(self):
        event_type = ModelFactory.create_event_type()

        response = self.client.get(reverse("events:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["event_types"], [repr(event_type)])
        self.assertQuerysetEqual(response.context["events"], [])

    def test_events_with_event_type_with_access(self):
        user = ModelFactory.create_user()
        event_type = ModelFactory.create_event_type()
        event = ModelFactory.create_event(
            name="custom event name",
            event_type=event_type,
            created_by=user,
            access_level=2,
        )

        response = self.client.get(reverse("events:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["event_types"], [repr(event_type)])
        self.assertQuerysetEqual(response.context["events"], [repr(event)])
    
    def test_events_with_event_type_without_access(self):
        user = ModelFactory.create_user()
        event_type = ModelFactory.create_event_type()
        event = ModelFactory.create_event(
            name="custom event name",
            event_type=event_type,
            created_by=user,
            access_level=1,
        )

        response = self.client.get(reverse("events:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["event_types"], [repr(event_type)])
        self.assertQuerysetEqual(response.context["events"], [])

    def test_event_types_ordered_by_type_ascending(self):
        num_event_types = 3
        event_types = [
            ModelFactory.create_event_type(type="custom event type {}".format(i))
            for i in range(1, 1 + num_event_types)
        ]

        response = self.client.get(reverse("events:index"))

        self.assertEqual(response.status_code, 200)
        expected = [repr(event_type) for event_type in event_types]
        actual = response.context["event_types"]
        self.assertQuerysetEqual(actual, expected)

    def test_events_ordered_by_start_time_descending(self):
        user = ModelFactory.create_user()
        event_type = ModelFactory.create_event_type()
        num_events = 3
        events = [
            ModelFactory.create_event(
                name="custom event {}".format(i),
                event_type=event_type,
                created_by=user,
                access_level=2,
            ) for i in range(1, 1 + num_events)]

        response = self.client.get(reverse("events:index"))

        self.assertEqual(response.status_code, 200)
        expected = [repr(event) for event in reversed(events)]
        actual = response.context["events"]
        self.assertQuerysetEqual(actual, expected)
