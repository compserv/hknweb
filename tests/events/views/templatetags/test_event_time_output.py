from django.test import TestCase

from datetime import datetime, timedelta
from hknweb.events.templatetags.event_filters import get_event_timerange


class TimestampOutputTests(TestCase):
    def test_returns_same_day_diff_time(self):
        start_time = datetime(year=2022, month=10, day=16, hour=10, minute=30)
        end_time = start_time + timedelta(hours=5)  # Same day, 15:30 --> 3:30 PM
        ans = "Sun, October 16, 2022 - 10:30 AM to 3:30 PM"
        result = get_event_timerange(start_time, end_time)
        self.assertEqual(result, ans)

    def test_returns_same_day_diff_time(self):
        start_time = datetime(year=2022, month=10, day=16, hour=10, minute=30)
        end_time = start_time + timedelta(days=3, hours=5)  # Oct 19, 15:30 --> 3:30 PM
        ans = "Sun, October 16, 2022 - 10:30 AM to Wed, October 19, 2022 - 3:30 PM"
        result = get_event_timerange(start_time, end_time)
        self.assertEqual(result, ans)

    def test_returns_same_day_diff_time_min_single_digit(self):
        start_time = datetime(year=2022, month=10, day=16, hour=10, minute=5)
        end_time = start_time + timedelta(hours=5)  # Same day, 15:05 --> 3:05 PM
        ans = "Sun, October 16, 2022 - 10:05 AM to 3:05 PM"
        result = get_event_timerange(start_time, end_time)
        self.assertEqual(result, ans)

    def test_returns_same_day_diff_time_min_single_digit(self):
        start_time = datetime(year=2022, month=10, day=16, hour=10, minute=5)
        end_time = start_time + timedelta(days=3, hours=5)  # Oct 19, 15:05 --> 3:05 PM
        ans = "Sun, October 16, 2022 - 10:05 AM to Wed, October 19, 2022 - 3:05 PM"
        result = get_event_timerange(start_time, end_time)
        self.assertEqual(result, ans)

    def test_returns_same_day_diff_time_min_single_digit_plus_few_mins(self):
        start_time = datetime(year=2022, month=10, day=16, hour=10, minute=5)
        end_time = start_time + timedelta(
            days=3, hours=5, minutes=3
        )  # Oct 19, 15:05 --> 3:05 PM
        ans = "Sun, October 16, 2022 - 10:05 AM to Wed, October 19, 2022 - 3:08 PM"
        result = get_event_timerange(start_time, end_time)
        self.assertEqual(result, ans)

    def test_returns_same_day_diff_time_min_to_double_digit(self):
        start_time = datetime(year=2022, month=10, day=16, hour=10, minute=5)
        end_time = start_time + timedelta(
            days=3, hours=5, minutes=12
        )  # Oct 19, 15:17 --> 3:17 PM
        ans = "Sun, October 16, 2022 - 10:05 AM to Wed, October 19, 2022 - 3:17 PM"
        result = get_event_timerange(start_time, end_time)
        self.assertEqual(result, ans)
