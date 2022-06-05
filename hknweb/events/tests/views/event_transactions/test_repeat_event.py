from datetime import datetime, timedelta
from django.test import TestCase

from django.urls import reverse

from hknweb.events.tests.views.event_transactions.utils import setUp
from hknweb.events.utils import generate_recurrence_times

class RepeatIntervalsUtilsTests(TestCase):

    def test_repeat_time_intervals_base_case(self):
        start_time = datetime(2022, 3, 15, 11, 30)
        end_time = datetime(2022, 3, 15, 3, 30)

        num_repeats = 0
        period = 0
        answer = [(datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30))]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="No repeat and No period")

        num_repeats = 1
        period = 0
        answer = [(datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30))]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="1 repeat and No period")

        num_repeats = 0
        period = 1
        answer = [(datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30))]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="No repeat and 1 week period")

    def test_repeat_time_intervals(self):
        start_time = datetime(2022, 3, 15, 11, 30)
        end_time = datetime(2022, 3, 15, 3, 30)

        num_repeats = 1
        period = 1
        answer = [
            (datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30)),
            (datetime(2022, 3, 15 + 7, 11, 30), datetime(2022, 3, 15 + 7, 3, 30)),
        ]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="1 repeat and 1 week period")

        num_repeats = 1
        period = 2
        answer = [
            (datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30)),
            (datetime(2022, 3, 15 + 14, 11, 30), datetime(2022, 3, 15 + 14, 3, 30)),
        ]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="1 repeat and 2 week period")

        num_repeats = 2
        period = 1
        answer = [
            (datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30)),
            (datetime(2022, 3, 15 + 7, 11, 30), datetime(2022, 3, 15 + 7, 3, 30)),
            (datetime(2022, 3, 15 + 14, 11, 30), datetime(2022, 3, 15 + 14, 3, 30)),
        ]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="2 repeat and 1 week period")

        num_repeats = 5
        period = 1
        answer = [
            (datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30)),
            (datetime(2022, 3, 15, 11, 30) + timedelta(7) , datetime(2022, 3, 15, 3, 30) + timedelta(7)),
            (datetime(2022, 3, 15, 11, 30) + timedelta(14), datetime(2022, 3, 15, 3, 30) + timedelta(14)),
            (datetime(2022, 3, 15, 11, 30) + timedelta(21), datetime(2022, 3, 15, 3, 30) + timedelta(21)),
            (datetime(2022, 3, 15, 11, 30) + timedelta(28), datetime(2022, 3, 15, 3, 30) + timedelta(28)),
            (datetime(2022, 3, 15, 11, 30) + timedelta(35), datetime(2022, 3, 15, 3, 30) + timedelta(35)),
        ]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="5 repeat and 1 week period")

        num_repeats = 5
        period = 3
        answer = [
            (datetime(2022, 3, 15, 11, 30), datetime(2022, 3, 15, 3, 30)),
            (datetime(2022, 3, 15, 11, 30) +  timedelta(21), datetime(2022, 3, 15, 3, 30) +  timedelta(21)),
            (datetime(2022, 3, 15, 11, 30) +  timedelta(42), datetime(2022, 3, 15, 3, 30) +  timedelta(42)),
            (datetime(2022, 3, 15, 11, 30) +  timedelta(63), datetime(2022, 3, 15, 3, 30) +  timedelta(63)),
            (datetime(2022, 3, 15, 11, 30) +  timedelta(84), datetime(2022, 3, 15, 3, 30) +  timedelta(84)),
            (datetime(2022, 3, 15, 11, 30) + timedelta(105), datetime(2022, 3, 15, 3, 30) + timedelta(105)),
        ]
        result = generate_recurrence_times(start_time, end_time, num_repeats, period)
        self.assertListEqual(result, answer, msg="5 repeat and 3 week period")
