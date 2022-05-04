from django.utils import timezone
from django.shortcuts import render

from hknweb.candidate.models import Announcement, Logistics, OffChallenge, BitByteActivity
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
    logistics.populate(request.user)

    context = {
        "user_self": True,
        "username": request.user.username,
        "announcements": Announcement.objects.filter(visible=True).order_by("-release_date"),
        "upcoming_events": upcoming_events,
        "logistics": logistics,
    }
    return render(request, "candidate/candidate_portal.html", context=context)
