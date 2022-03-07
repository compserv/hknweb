from django.shortcuts import render, redirect
from django.contrib import messages

from hknweb.utils import login_and_permission
from hknweb.events.models import Event
from hknweb.events.forms import AttendanceFormForm


@login_and_permission("events.add_attendanceform")
def attendance(request, event_id):
    form = AttendanceFormForm(request.POST or None)
    if request.method == "POST":
        form.data = form.data.copy()
        form.data["event"] = event_id

        if form.is_valid():
            form.save()

            messages.success(request, "Attendance form has been added!")
            return redirect("events:detail", id=event_id)
        else:
            messages.error(request, form.errors)

    return render(request, "events/attendance.html", {"form": form})
