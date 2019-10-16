from django.shortcuts import render
from hknweb.events.models import Event
from hknweb.tutoring.models import Tutor
from django.utils import timezone
import datetime
import pytz


def home(request):
    today = timezone.now()
    # today = datetime.datetime.now()
    # next_weekday = today
    # TODO: determine earliest weekday for which tutoring still has yet to complete, and query those tutors
    # tutors = 
    
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    def two_digits(minutes):
        if minutes < 10:
            return '0' + str(minutes)
        return str(minutes)
    def parse_date(event):
        timezone.activate(pytz.timezone('America/Los_Angeles'))
        tz = pytz.timezone('America/Los_Angeles')
        start = tz.normalize(event.start_time.astimezone(tz))
        end = tz.normalize(event.end_time.astimezone(tz))
        start_timetuple, end_timetuple = start.timetuple(), end.timetuple()
        start_day = weekdays[start_timetuple[6]] + '  ' + str(start_timetuple[1]) + '/' + str(start_timetuple[2])
        end_day = weekdays[end_timetuple[6]] + '  ' + str(end_timetuple[1]) + '/' + str(end_timetuple[2])
        start_time = start_day + '  ' + format_time(start_timetuple[3], start_timetuple[4])
        if (start_day == end_day):
            end_time = '  ' + format_time(end_timetuple[3], end_timetuple[4])
        else:
            end_time = '  ' + end_day + '  ' + format_time(end_timetuple[3], end_timetuple[4])
        return {'start': start_time, 'end': end_time}

    def format_time(hour, min):
        if hour == 0:
            return "12:" + two_digits(min) + " AM  "
        elif hour > 12:
            return str(hour - 12) + ":" + two_digits(min) + " PM  "
        elif hour == 12:
            return "12:" + two_digits(min) + " PM  "
        else:
            return str(hour) + ":" + two_digits(min) + " AM  "

    upcoming_events = Event.objects.filter(start_time__gte=today).order_by('start_time')[:4]
    events = []
    for event in upcoming_events:
        temp_dict = parse_date(event)
        temp_dict['name'] = event.name
        events.append(temp_dict)
    context = {
        # 'tutors': tutors,
        'events': events,
    }
    return render(request, 'landing/home.html', context)
