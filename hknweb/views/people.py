from django.shortcuts import render
from django.db.models import QuerySet, F, BooleanField, Value
from django.contrib.auth.models import User

from hknweb.utils import allow_public_access, get_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.models import Election, Committeeship
from hknweb.forms import ProfilePictureForm


@allow_public_access
def people(request):
    election: Election = Election.objects.last()
    committeeships: QuerySet[Committeeship] = \
        election.committeeship_set \
            .annotate(is_execs=Value(F("committee__name") == "Execs", output_field=BooleanField())) \
            .order_by("-is_execs", "committee__name")

    is_officer = get_access_level(request.user) <= GROUP_TO_ACCESSLEVEL["officer"]
    form = ProfilePictureForm(request.POST)
    if is_officer and request.method == "POST":
        user = User.objects.get(pk=request.POST["user_id"])
        form.instance = user.profile
        if form.is_valid():
            form.save()

    context = {
        "committeeships": committeeships,
        "semester": election.semester,
        "is_officer": is_officer,
        "form": form,
    }
    return render(request, "about/people.html", context=context)
