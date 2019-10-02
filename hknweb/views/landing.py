from django.shortcuts import render
from hknweb.events.models import Event
from hknweb.tutoring.models import Tutor
import datetime



import pprint

def home(request):
    today = datetime.datetime.now()
    next_weekday = today
    # TODO: determine earliest weekday for which tutoring still has yet to complete, and query those tutors
    # tutors = 
    
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    def two_digits(minutes):
        if len(minutes) == 1:
            return '0' + minutes
        return minutes
    def parse_date(date_time_obj):
        start, end = date_time_obj.start_time, date_time_obj.end_time
        start_timetuple, end_timetuple = start.timetuple(), end.timetuple()
        day = weekdays[start_timetuple[6]] + ' ' + str(start_timetuple[1]) + '/' + str(start_timetuple[2])
        start_time = str(start_timetuple[3]) + ':' + two_digits(str(start_timetuple[4]))
        if start_timetuple[2] == end_timetuple[2]:
            end_time = str(end_timetuple[3]) + ':' + two_digits(str(end_timetuple[4]))
        else:
            end_time = 'overnight'
        return {'day': day, 'start': start_time, 'end': end_time}
    upcoming_events = Event.objects.filter(start_time__gte=today).order_by('start_time')
    if len(upcoming_events) > 4:
        upcoming_events = upcoming_events[:4]
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
