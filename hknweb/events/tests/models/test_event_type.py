from django.test import TestCase

from hknweb.events.tests.models.utils import ModelFactory


class EventTypeModelTests(TestCase):
    def setUp(self):
        event_type = ModelFactory.create_event_type()

        self.event_type = event_type

    def test_repr(self):
        expected = "EventType(type={})".format(self.event_type.type)
        actual = repr(self.event_type)

        self.assertEqual(expected, actual)

    def test_str(self):
        expected = str(self.event_type.type)
        actual = str(self.event_type)

        self.assertEqual(expected, actual)
