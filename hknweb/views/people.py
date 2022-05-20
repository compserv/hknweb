from django.shortcuts import render
from django.db.models import QuerySet, F, BooleanField, Value

from hknweb.utils import allow_public_access

from hknweb.models import Election, Committeeship


@allow_public_access
def people(request):
    election: Election = Election.objects.last()
    committeeships: QuerySet[Committeeship] = \
        election.committeeship_set \
            .annotate(is_execs=Value(F("committee__name") == "Execs", output_field=BooleanField())) \
            .order_by("-is_execs", "committee__name")

    context = {
        "committeeships": committeeships,
        "semester": election.semester,
    }
    return render(request, "about/people.html", context=context)
