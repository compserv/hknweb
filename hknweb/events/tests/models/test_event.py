import datetime

from django.utils import timezone

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

    def test_repr(self):
        expected = "Event(name={}, location={})".format(
            self.event_name,
            self.event.location,
        )
        actual = repr(self.event)

        self.assertEqual(expected, actual)

    def test_str(self):
        expected = "{} - {} to {}".format(
            self.event_name,
            self.event.start_time,
            self.event.end_time,
        )
        actual = str(self.event)

        self.assertEqual(expected, actual)

    def test_get_absolute_url(self):
        expected = "/events/{}".format(self.event.id)
        actual = self.event.get_absolute_url()

        self.assertEqual(expected, actual)

    def test_semester_with_month_lt_7_returns_spring(self):
        current_time = timezone.now()
        time = datetime.datetime(
            year=current_time.year,
            month=6,
            day=current_time.day,
        )
        self.event.start_time = time

        expected = "{} {}".format("Spring", time.year)
        actual = self.event.semester

        self.assertEqual(expected, actual)

    def test_semester_with_month_geq_7_returns_fall(self):
        current_time = timezone.now()
        time = datetime.datetime(
            year=current_time.year,
            month=7,
            day=current_time.day,
        )
        self.event.start_time = time

        expected = "{} {}".format("Fall", time.year)
        actual = self.event.semester

        self.assertEqual(expected, actual)

    def test_on_waitlist_without_waitlist_returns_false(self):
        self.assertFalse(self.event.on_waitlist(None))
