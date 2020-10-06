from datetime import datetime

from .constants import (
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
