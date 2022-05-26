from django.shortcuts import render
from django.utils import timezone
from django.db.models import Value, DateTimeField

from hknweb.tutoring.models import TutoringLogistics


def index(request):
    context = {
        "offset": timezone.now(),
    }

    logistics: TutoringLogistics = TutoringLogistics.objects \
        .order_by("-semester__year", "semester__semester") \
        .first()
    if logistics is not None:
        context["slots"] = \
            logistics.slot_set.all() \
                .prefetch_related("tutors") \
                .annotate(offset=Value(context["offset"], output_field=DateTimeField()))

    return render(request, "tutoring/index.html", context=context)
