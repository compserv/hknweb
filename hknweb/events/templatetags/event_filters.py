from django import template
import bleach
from django.conf import settings
from pytz import timezone

register = template.Library()


@register.filter
def event_name(name):
    return bleach.clean(name, tags=[], strip=True)

# Made like this to make it compadible with Windows + Linux
#  Leading zero syntax on strftime has a difference ("#" and "-")
def get_time_string(dt):
    hour = dt.hour
    mins = dt.minute
    ampm = dt.strftime("%p")
    return f"{hour}:{mins} {ampm}"

def get_date_string(dt):
    weekday = dt.strftime("%a")
    month = dt.strftime("%B")
    day = dt.day
    year = dt.year
    clock_time = get_time_string(dt)
    return f"{weekday}, {month} {day}, {year} - {clock_time}"

@register.filter
def process_event_time(event):
    settings_time_zone = timezone(settings.TIME_ZONE)
    start_time_entry = event.start_time.astimezone(settings_time_zone)
    end_time_entry = event.end_time.astimezone(settings_time_zone)
    start_date_time = get_date_string(start_time_entry)
    if start_time_entry.date() == end_time_entry.date():
        end_date_time = get_time_string(end_time_entry)
    else:
        end_date_time = get_date_string(end_time_entry)
    return "{} to {}".format(start_date_time, end_date_time)
