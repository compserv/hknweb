from django.shortcuts import render, redirect
from django.contrib import messages

from hknweb.utils import login_and_permission
from hknweb.events.constants import ATTR
from hknweb.events.forms import EventForm
from hknweb.events.utils import (
    create_event,
    generate_recurrence_times,
)


@login_and_permission("events.add_event")
def add_event(request):
    form = EventForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data

            times = generate_recurrence_times(
                data["start_time"],
                data["end_time"],
                data["recurring_num_times"],
                data["recurring_period"],
            )

            for start_time, end_time in times:
                create_event(data, start_time, end_time, request.user)

            messages.success(request, "Event has been added!")
            return redirect("/events")
        else:
            messages.error(request, "Something went wrong oops")
    return render(request, "events/event_add.html", {"form": form})
