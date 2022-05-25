from django.shortcuts import render

from hknweb.tutoring.models import TutoringLogistics


def index(request):
    context = {}

    logistics: TutoringLogistics = TutoringLogistics.objects \
        .order_by("-semester__year", "semester__semester") \
        .first()
    if logistics is not None:
        context["slots"] = logistics.slot_set.all().prefetch_related("tutors")

    return render(request, "tutoring/index.html", context=context)
