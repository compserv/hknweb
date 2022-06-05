from datetime import datetime, timedelta
from threading import Thread

from django import forms
from django.core.validators import URLValidator
from django.utils.safestring import mark_safe

from hknweb.events.constants import ATTR
from hknweb.events.models import Event


def create_event(data, start_time, end_time, user):
    event = Event.objects.create(
        name=data[ATTR.NAME],
        start_time=start_time,
        end_time=end_time,
        location=data[ATTR.LOCATION],
        event_type=data[ATTR.EVENT_TYPE],
        description=data[ATTR.DESCRIPTION],
        rsvp_limit=data[ATTR.RSVP_LIMIT],
        access_level=data[ATTR.ACCESS_LEVEL],
        created_by=user,
    )
    event.save()


def generate_recurrence_times(
    start_time: datetime, end_time: datetime, num_repeats: int, period: int
) -> list:
    """
    Parameters
    ----------
    start_time: datetime
        The datetime of the starting time (day and clock time)
    end_time: datetime
        The datetime of the ending time (day and clock time)
    num_repeats: int
        The number of times to repeat the event
    period: int
        The number of weeks between each occurrence, in weeks.

    Returns
    ----------
    List of (start_time, end_time) for each event occurance (including first occurance)
    """
    times = [(start_time, end_time)]
    if num_repeats <= 0 or period <= 0:
        return times
    time_diff = timedelta(period * 7)
    for _ in range(num_repeats):
        start_time, end_time = start_time + time_diff, end_time + time_diff
        times.append((start_time, end_time))
    return times


DATETIME_WIDGET_NO_AUTOCOMPLETE = forms.DateTimeInput(attrs={"autocomplete": "off"})


def format_url(s: str, max_width: int = None) -> str:
    url_validator = URLValidator()
    try:
        url_validator(s)
        link_with_tag = (
            "<a href='{link}' style='background-color: white'> {link} </a>".format(
                link=s
            )
        )
        return mark_safe(link_with_tag)
    except:  # lgtm [py/catch-base-exception]
        return s


class SingleThreadWrapper(Thread):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        self.fn()
