from django import template
import bleach
from django.conf import settings
from pytz import timezone
from datetime import datetime

register = template.Library()


@register.filter
def event_name(name):
    return bleach.clean(name, tags=[], strip=True)


def military_hour_to_hour(hour):
    assert (0 <= hour) and (hour <= 23), "Hour outside of military time"
    if hour == 0:
        # Midnight
        return 12
    elif hour <= 12:
        # But more than 0
        return hour
    else:
        # hour > 12
        return hour - 12


# Made like this to make it compadible with Windows + Linux
#  Leading zero syntax on strftime has a difference ("#" and "-")
def get_time_string(dt):
    hour = military_hour_to_hour(dt.hour)
    mins = dt.minute
    ampm = dt.strftime("%p")
    return f"{hour}:{mins:02} {ampm}"


def get_date_string(dt):
    weekday = dt.strftime("%a")
    month = dt.strftime("%B")
    day = dt.day
    year = dt.year
    clock_time = get_time_string(dt)
    return f"{weekday}, {month} {day}, {year} - {clock_time}"


def get_event_timerange(start_time: datetime, end_time: datetime):
    start_time_str = get_date_string(start_time)
    end_time_str = ""
    if start_time.date() == end_time.date():
        end_time_str = get_time_string(end_time)
    else:
        end_time_str = get_date_string(end_time)
    return "{} to {}".format(start_time_str, end_time_str)


@register.filter
def process_event_time(event):
    settings_time_zone = timezone(settings.TIME_ZONE)
    start_time = event.start_time.astimezone(settings_time_zone)
    end_time = event.end_time.astimezone(settings_time_zone)
    return get_event_timerange(start_time, end_time)
