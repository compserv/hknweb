import urllib.parse

from django.urls import reverse
from django.utils import timezone

from tests.tutoring.views.test_index import TuteeViewTestHelper


class SlotsViewTests(TuteeViewTestHelper):
    def test_slots_returns_200(self):
        filter_str = "course_filter=&tutor_filter=&start=2022-05-31T00%3A00%3A00-07%3A00&end=2022-06-01T00%3A00%3A00-07%3A00"
        response = self.client.get(reverse("tutoring:slots") + f"?{filter_str}")

        self.assertEqual(response.status_code, 200)

    def test_slots_filter_returns_200(self):
        filter_str = "course_filter=&tutor_filter=0&start=2022-05-31T00%3A00%3A00-07%3A00&end=2022-06-01T00%3A00%3A00-07%3A00"
        response = self.client.get(reverse("tutoring:slots") + f"?{filter_str}")

        self.assertEqual(response.status_code, 200)

    def test_slots_display_day_returns_200(self):
        now = timezone.now()
        to_default_hour = lambda h, m, s: timezone.datetime(
            now.year, now.month, now.day, h, m, s
        )
        to_iso_url_str = lambda t: urllib.parse.quote_plus(t.isoformat())
        start = to_iso_url_str(to_default_hour(0, 0, 0))
        end = to_iso_url_str(to_default_hour(23, 59, 59))

        filter_str = f"course_filter=&tutor_filter=&start={start}&end={end}"
        response = self.client.get(reverse("tutoring:slots") + f"?{filter_str}")

        self.assertEqual(response.status_code, 200)
