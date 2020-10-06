from django.shortcuts import render
from django.utils import timezone
from hknweb.models import Announcement

from hknweb.events.models import Event
from hknweb.reviewsessions.models import ReviewSession
# from hknweb.tutoring.models import Tutor

from hknweb.models import Announcement


def home(request):
    # TODO: determine earliest weekday for which tutoring still has yet to complete, and query those tutors
    num_events = 4
    upcoming_events = Event.objects.filter(end_time__gte=timezone.now()) \
        .order_by('start_time')[:num_events]
    upcoming_review_sessions = ReviewSession.objects.filter(end_time__gte=timezone.now()) \
        .order_by('start_time')[:num_events]
    announcements = Announcement.objects \
        .filter(visible=True) \
        .order_by('-release_date')

    context = {
        # 'tutors': tutors,
        'events': upcoming_events,
        'announcements' : announcements,
        'reviewsessions' : upcoming_review_sessions,
    }
    return render(request, 'landing/home.html', context)

def about(request):
    return render(request, 'about/abouthkn.html')
