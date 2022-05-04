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
    rsvps = Rsvp.objects.filter(user=request.user)

    logistics.event_req_objs = logistics.event_reqs.all()
    for event_req in logistics.event_req_objs:
        event_req_rsvps = rsvps.filter(event__event_type__in=event_req.event_types.all())
        event_req.confirmed = [r.event for r in event_req_rsvps.filter(confirmed=True)]
        event_req.unconfirmed = [r.event for r in event_req_rsvps.filter(confirmed=False)]
        event_req.n_finished = len(event_req.confirmed)
    logistics.event_reqs_finished = all(e.n_finished >= e.n for e in logistics.event_req_objs)

    logistics.forms_confirmed = logistics.form_reqs.filter(completed__in=[request.user])
    logistics.forms_unconfirmed = logistics.form_reqs.exclude(completed__in=[request.user])
    logistics.misc_confirmed = logistics.misc_reqs.filter(completed__in=[request.user])
    logistics.misc_unconfirmed = logistics.misc_reqs.exclude(completed__in=[request.user])

    challenges = OffChallenge.objects.filter(requester=request.user)
    logistics.n_challenges_confirmed = sum(c.confirmed for c in challenges)
    logistics.n_challenges_rejected = sum(c.rejected for c in challenges)
    logistics.n_challenges_pending = \
        challenges.count() - logistics.n_challenges_confirmed - logistics.n_challenges_rejected

    hangouts = rsvps.filter(event__event_type__type="Hangout")
    logistics.hangouts_confirmed = [r.event for r in hangouts.filter(confirmed=True)]
    logistics.hangouts_unconfirmed = [r.event for r in hangouts.filter(confirmed=False)]

    logistics.n_interactivities = len(logistics.hangouts_confirmed) + logistics.n_challenges_confirmed

    logistics.n_bitbyte = BitByteActivity.objects \
        .filter(participants__in=[request.user], confirmed=True).count()

    context = {
        "user_self": True,
        "username": request.user.username,
        "announcements": Announcement.objects.filter(visible=True).order_by("-release_date"),
        "upcoming_events": upcoming_events,
        "logistics": logistics,
    }
    return render(request, "candidate/candidate_portal.html", context=context)
