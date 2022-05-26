from django.shortcuts import render
from django.utils import timezone
from django.db.models import Value, DateTimeField

from hknweb.tutoring.models import TutoringLogistics


def index(request):
    nav = request.GET.get("nav", "0")
    try:
        nav = int(nav)
    except ValueError:
        nav = 0

    context = {
        "offset": timezone.now() + timezone.timedelta(weeks=nav),
    }
    print(context["offset"])

    logistics: TutoringLogistics = TutoringLogistics.objects \
        .order_by("-semester__year", "semester__semester") \
        .first()
    if logistics is not None:
        context["slots"] = \
            logistics.slot_set.all() \
                .prefetch_related("tutors") \
                .annotate(offset=Value(context["offset"], output_field=DateTimeField()))

    return render(request, "tutoring/index.html", context=context)
