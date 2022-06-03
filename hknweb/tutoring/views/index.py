from django.shortcuts import render
from django.utils import timezone

from hknweb.utils import allow_public_access

from hknweb.tutoring.forms import CourseFilterForm


@allow_public_access
def index(request):
    nav = request.GET.get("nav", "0")
    try:
        nav = int(nav)
    except ValueError:
        nav = 0

    context = {
        "offset": timezone.now() + timezone.timedelta(days=nav),
        "form": CourseFilterForm(),
    }

    return render(request, "tutoring/index.html", context=context)
