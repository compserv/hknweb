from django.test import TestCase

from hknweb.events.tests.models.utils import ModelFactory


class EventModelTests(TestCase):
    def setUp(self):
        user = ModelFactory.create_user()
        event_type = ModelFactory.create_event_type()
        event_name = "custom event name"

        event = ModelFactory.create_event(
            name=event_name,
            event_type=event_type,
            created_by=user,
        )

        self.user = user
        self.event_type = event_type
        self.event_name = event_name
        self.event = event

    def test_default_event_creation(self):
        self.assertIs(self.user, self.event.created_by)
        self.assertIs(self.event_type, self.event.event_type)
        self.assertIs(self.event_name, self.event.name)
