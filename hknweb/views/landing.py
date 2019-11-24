from django.shortcuts import render
from django.utils import timezone

from hknweb.events.models import Event
# from hknweb.tutoring.models import Tutor


def home(request):
    # TODO: determine earliest weekday for which tutoring still has yet to complete, and query those tutors
    num_events = 4
    upcoming_events = Event.objects.filter(end_time__gte=timezone.now()) \
        .order_by('start_time')[:num_events]
    context = {
        # 'tutors': tutors,
        'events': upcoming_events,
    }
    return render(request, 'landing/home.html', context)
