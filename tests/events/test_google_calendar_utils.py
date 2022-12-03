from django.test import TestCase

from hknweb.events.google_calendar_utils import (
    create_event_resource,
    get_calendar_link,
    check_credentials_wrapper,
)
from hknweb.events.models.google_calendar import GoogleCalendarCredentials


class GoogleCalendarUtilsTests(TestCase):
    def test_create_event_resource(self):
        expected = {
            "summary": "test_summary",
            "location": "test_location",
            "description": "test_description",
            "start": {
                "dateTime": "time_start",
                "timeZone": "America/Los_Angeles",
            },
            "end": {
                "dateTime": "time_end",
                "timeZone": "America/Los_Angeles",
            },
        }
        actual = create_event_resource(
            summary="test_summary",
            location="test_location",
            description="test_description",
            start="time_start",
            end="time_end",
        )

        self.assertDictEqual(expected, actual)

    def test_get_calendar_link(self):
        self.assertTrue(get_calendar_link("test_calendar_id"))

    def test_check_credentials_wrapper_returns_false(self):
        GoogleCalendarCredentials.objects.create(file="my_file.json")
        check_credentials_wrapper(lambda: 2)()
