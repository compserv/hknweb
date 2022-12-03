from django.shortcuts import render
from django.utils import timezone
from django.db.models import Min, Max
from django.utils import timezone

from hknweb.utils import allow_public_access, PACIFIC_TIMEZONE

from hknweb.tutoring.forms import CourseFilterForm, TutorFilterForm
from hknweb.tutoring.models import TutoringLogistics


@allow_public_access
def index(request):
    nav = request.GET.get("nav", "0")
    try:
        nav = int(nav)
    except ValueError:
        nav = 0

    logistics = TutoringLogistics.get_most_recent()
    now = timezone.datetime.now(tz=PACIFIC_TIMEZONE)
    times = {
        "calendar_start_time": now.replace(hour=9, minute=0),
        "calendar_end_time": now.replace(hour=17, minute=0),
    }
    if logistics:
        slot_times = logistics.slot_set.values_list("time", flat=True).aggregate(
            calendar_start_time=Min("time"),
            calendar_end_time=Max("time"),
        )

        replace_hour = lambda t, offset: t.replace(
            hour=min(23, max(0, t.hour + offset))
        )
        times["calendar_start_time"] = replace_hour(
            slot_times["calendar_start_time"], -1
        )
        times["calendar_end_time"] = replace_hour(slot_times["calendar_end_time"], 2)

    form = CourseFilterForm()
    form.fields.update(TutorFilterForm().fields)
    context = {
        "offset": timezone.now() + timezone.timedelta(days=nav),
        "form": form,
        **times,
    }

    return render(request, "tutoring/index.html", context=context)
