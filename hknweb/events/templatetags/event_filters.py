from django import template
import bleach
from django.conf import settings
from pytz import timezone

register = template.Library()


@register.filter
def event_name(name):
    return bleach.clean(name, tags=[], strip=True)

@register.filter
def process_event_time(event):
    settings_time_zone = timezone(settings.TIME_ZONE)
    start_time_entry = event.start_time.astimezone(settings_time_zone)
    end_time_entry = event.end_time.astimezone(settings_time_zone)
    start_date_time = start_time_entry.strftime("%a, %B %-d, %Y - %-I:%M %p")
    if (start_time_entry.date() == end_time_entry.date()):
        end_date_time = end_time_entry.strftime("%-I:%M %p")
    else:
        end_date_time = end_time_entry.strftime("%a, %B %-d, %Y - %-I:%M %p")
    return "{} to {}".format(start_date_time, end_date_time)
