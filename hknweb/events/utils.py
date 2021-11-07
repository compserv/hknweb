from datetime import datetime, timedelta

from django import forms
from django.core.validators import URLValidator
from django.utils.safestring import mark_safe
import urllib.parse

from .constants import (
    ATTR,
    DAY_ATTRIBUTE_NAME,
    DESCRIPTION_ATTRIBUTE_NAME,
    END_TIME_ATTRIBUTE_NAME,
    EVENT_NAME_ATTRIBUTE_NAME,
    GCAL_DATETIME_TEMPLATE,
    GCAL_INVITE_TEMPLATE,
    HOUR_ATTRIBUTE_NAME,
    LOCATION_ATTRIBUTE_NAME,
    MINUTES_ATTRIBUTE_NAME,
    MONTH_ATTRIBUTE_NAME,
    SECONDS_ATTRIBUTE_NAME,
    START_TIME_ATTRIBUTE_NAME,
    YEAR_ATTRIBUTE_NAME,
)
from .models import Event


def create_gcal_link(event: Event) -> str:
    attrs = {
        EVENT_NAME_ATTRIBUTE_NAME: urllib.parse.quote_plus(event.name, safe=''),
        DESCRIPTION_ATTRIBUTE_NAME: urllib.parse.quote_plus(event.description, safe=''),
        LOCATION_ATTRIBUTE_NAME: urllib.parse.quote_plus(event.location, safe=''),
        START_TIME_ATTRIBUTE_NAME: format_gcal_time(event.start_time),
        END_TIME_ATTRIBUTE_NAME: format_gcal_time(event.end_time),
    }
    return GCAL_INVITE_TEMPLATE.format(**attrs)


def format_gcal_time(time: datetime) -> str:
    attrs = {
        YEAR_ATTRIBUTE_NAME: time.year,
        MONTH_ATTRIBUTE_NAME: time.month,
        DAY_ATTRIBUTE_NAME: time.day,
        HOUR_ATTRIBUTE_NAME: time.hour,
        MINUTES_ATTRIBUTE_NAME: time.minute,
        SECONDS_ATTRIBUTE_NAME: time.second,
    }
    return GCAL_DATETIME_TEMPLATE.format(**attrs)


def generate_repeated_slug(base_slug, start_time, end_time):
    return "{base_slug}-{start_time}-{end_time}".format(
        base_slug=base_slug,
        start_time=format_gcal_time(start_time),
        end_time=format_gcal_time(end_time),
    )


def create_event(data, start_time, end_time, user):
    event = Event.objects.create(
        name=data[ATTR.NAME],
        slug=generate_repeated_slug(data[ATTR.SLUG], start_time, end_time),
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
    start_time: datetime, end_time: datetime, num_times: int, period: int
) -> list:
    """
    Parameters
    ----------
    period: int
        The number of weeks between each occurrence, in weeks.

    """
    times = [(start_time, end_time)]
    if num_times <= 0 or period <= 0:
        return times
    time_diff = timedelta(period * 7)
    for _ in range(num_times - 1):
        start_time, end_time = start_time + time_diff, end_time + time_diff
        times.append((start_time, end_time))
    return times


def get_padding(l1, l2):
    l1, l2 = max(l1, 1), max(l2, 1)
    p1, p2 = max(l1 - l2, 0), max(l2 - l1, 0)
    return [None] * (p1 + 1), [None] * (p2 + 1)


DATETIME_WIDGET_NO_AUTOCOMPLETE = forms.DateTimeInput(attrs={"autocomplete": "off"})


def format_url(s: str, max_width: int = None) -> str:
    url_validator = URLValidator()
    try:
        url_validator(s)
        link_with_tag = "<a href='{link}' style='background-color: white'> {link} </a>".format(
            link=s
        )
        return mark_safe(link_with_tag)
    except:
        return s
