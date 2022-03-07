from django.shortcuts import render
from django.contrib import messages

from hknweb.utils import login_and_permission
from hknweb.events.models import AttendanceForm
from hknweb.events.forms import AttendanceFormForm


@login_and_permission("events.add_attendanceform")
def attendance(request, event_id):
    forms = AttendanceForm.objects.filter(event=event_id)
    instance = forms.first() if forms.exists() else None
    form = AttendanceFormForm(request.POST or None, instance=instance)

    if request.method == "POST":
        form.data = form.data.copy()
        form.data["event"] = event_id

        if form.is_valid():
            form.save()
            messages.success(request, "Attendance form saved!")
        else:
            messages.error(request, form.errors)

    return render(request, "events/attendance.html", {"form": form})
