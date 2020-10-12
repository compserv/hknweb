from datetime import datetime, timedelta

from .constants import (
    ATTR,
    DAY_ATTRIBUTE_NAME,
    DESCRIPTION_ATTRIBUTE_NAME,
    END_TIME_ATTRIBUTE_NAME,
    EVENT_NAME_ATTRIBUTE_NAME,
    GCAL_DATETIME_TEMPLATE,
    GCAL_INVITE_TEMPLATE,
    GROUP_TO_ACCESSLEVEL,
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
        EVENT_NAME_ATTRIBUTE_NAME: event.name,
        START_TIME_ATTRIBUTE_NAME: format_gcal_time(event.start_time),
        END_TIME_ATTRIBUTE_NAME: format_gcal_time(event.end_time),
        DESCRIPTION_ATTRIBUTE_NAME: event.description,
        LOCATION_ATTRIBUTE_NAME: event.location,
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


def generate_recurrence_times(start_time: datetime, end_time: datetime, num_times: int, period: int) -> list:
    """
    Parameters
    ----------
    period: int
        The number of weeks between each occurrence, in weeks.

    """
    times = [(start_time, end_time)]
    if num_times <= 0 or period <= 0: return times
    time_diff = timedelta(period * 7)
    for _ in range(num_times - 1):
        start_time, end_time = start_time + time_diff, end_time + time_diff
        times.append((start_time, end_time))
    return times


def get_padding(l1, l2):
    l1, l2 = max(l1, 1), max(l2, 1)
    p1, p2 = max(l1 - l2, 0), max(l2 - l1, 0)
    return [None] * (p1 + 1), [None] * (p2 + 1)


def get_access_level(user):
    access_level = 2  # See constants.py
    for group_name, access_value in GROUP_TO_ACCESSLEVEL.items():
        if user.groups.filter(name=group_name).exists():
            access_level = min(access_level, access_value)
    return access_level
