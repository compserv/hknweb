from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from hknweb.candidate.models import Announcement, Logistics
from hknweb.events.models import Event
from hknweb.coursesemester.models import Semester

from hknweb.candidate.forms import BitByteRequestForm

from hknweb.utils import get_access_level

from hknweb.utils import (
    GROUP_TO_ACCESSLEVEL,
    login_and_access_level,
)


def user_candidate_portal(user: User) -> dict:    
    semester = Semester.objects.order_by("year", "-semester").last()
    logistics: Logistics = Logistics.objects.filter(semester=semester).first()
    logistics.populate(user)

    return {
        "username": user.username,
        "logistics": logistics,
    }


@login_and_access_level(GROUP_TO_ACCESSLEVEL["member"])
def candidate_portal_view_by_username(request, username):
    user = User.objects.filter(username=username).first()
    if user is None:
        messages.warning(request, "User {} does not exist.".format(username))
        return redirect("candidate:candidate_portal")

    context = {
        "user_self": False,
        **user_candidate_portal(user),
    }
    return render(request, "candidate/candidate_portal.html", context=context)


@login_and_access_level(GROUP_TO_ACCESSLEVEL["candidate"])
def candidate_portal(request):
    today = timezone.now()
    upcoming_events = Event.objects \
        .filter(
            start_time__range=(today, today + timezone.timedelta(days=7)),
            access_level__gte=get_access_level(request.user),) \
        .order_by("start_time")

    context = {
        "user_self": True,
        "announcements": Announcement.objects.filter(visible=True).order_by("-release_date"),
        "upcoming_events": upcoming_events,
        **user_candidate_portal(request.user),
        "form": BitByteRequestForm(),
    }
    return render(request, "candidate/candidate_portal.html", context=context)
