from django.utils import timezone
from django.shortcuts import render

from hknweb.candidate.models import Announcement, Logistics
from hknweb.events.models import Event, Rsvp
from hknweb.coursesemester.models import Semester

from hknweb.utils import get_access_level

from hknweb.utils import (
    GROUP_TO_ACCESSLEVEL,
    login_and_access_level,
)


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def candidate_portal(request):
    today = timezone.now()
    upcoming_events = Event.objects \
        .filter(
            start_time__range=(today, today + timezone.timedelta(days=7)),
            access_level__gte=get_access_level(request.user),) \
        .order_by("start_time")

    semester = Semester.objects.order_by("year", "-semester").last()
    logistics = Logistics.objects.filter(semester=semester).first()

    event_reqs = logistics.event_reqs.all()
    rsvps = Rsvp.objects.filter(user=request.user)
    for event_req in event_reqs:
        event_req_rsvps = rsvps.filter(event__event_type__in=event_req.event_types.all())
        event_req.confirmed = [r.event for r in event_req_rsvps.filter(confirmed=True)]
        event_req.unconfirmed = [r.event for r in event_req_rsvps.filter(confirmed=False)]
        event_req.n_finished = len(event_req.confirmed)

    context = {
        "user_self": True,
        "username": request.user.username,
        "announcements": Announcement.objects.filter(visible=True).order_by("-release_date"),
        "upcoming_events": upcoming_events,
        "event_reqs": event_reqs,
    }
    return render(request, "candidate/candidate_portal.html", context=context)
