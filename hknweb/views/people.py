from django.shortcuts import render
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.http import Http404
from django.conf import settings
from django.core.exceptions import PermissionDenied

from hknweb.utils import allow_public_access, get_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.models import Election, Committeeship
from hknweb.forms import ProfilePictureForm, SemesterSelectForm

from hknweb.coursesemester.models import Semester


@allow_public_access
def people(request):
    if "semester" in request.GET and not request.GET["semester"].isdigit():
        raise Http404

    is_bridge = request.user.groups.filter(name=settings.BRIDGE_GROUP)

    # Prevents unauthorized users from just typing the url to edit the page
    if request.GET.get("edit") == "true":
        if not is_bridge:
            raise PermissionDenied

    semester: Semester = Semester.objects.filter(
        pk=request.GET.get("semester") or None
    ).first()
    if semester is None:
        # If the requested semester is invalid, default to the latest semester with election
        semester = (
            Semester.objects.exclude(election=None)
            .order_by("-year", "semester")
            .first()
        )

    if semester is None or not semester.election_set.exists():
        execs = None
        committeeships = None
    else:
        election: Election = semester.election_set.first()

        execs: QuerySet[Committeeship] = election.committeeship_set.filter(
            committee__is_exec=True
        ).order_by("committee__name")
        committeeships: QuerySet[Committeeship] = election.committeeship_set.filter(
            committee__is_exec=False
        ).order_by("committee__name")

    form = ProfilePictureForm(request.POST)
    if is_bridge and request.method == "POST":
        user = User.objects.get(pk=request.POST["user_id"])
        form.instance = user.profile
        if form.is_valid():
            form.save()

    context = {
        "execs": execs,
        "committeeships": committeeships,
        "form": form,
        "semester_select_form": SemesterSelectForm({"semester": semester}),
    }

    return render(request, "about/people.html", context=context)
