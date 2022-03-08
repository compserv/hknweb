from django.shortcuts import render, redirect
from django.contrib import messages

from hknweb.utils import login_and_permission
from hknweb.events.models import AttendanceForm
from hknweb.events.forms import AttendanceFormForm


@login_and_permission("events.add_attendanceform")
def manage_attendance(request, event_id):
    forms = AttendanceForm.objects.filter(event=event_id)
    instance = forms.first() if forms.exists() else None
    form = AttendanceFormForm(request.POST or None, instance=instance)

    if request.method == "POST":
        form.data = form.data.copy()
        form.data["event"] = event_id

        if form.is_valid():
            form.save()
            messages.success(request, "Attendance form saved!")
            return redirect("events:detail", id=event_id)

    if instance:
        feedback = [r.feedback for r in instance.attendanceresponse_set.all()]
    else:
        feedback = None

    context = {
        "form": form,
        "feedback": feedback,
    }
    return render(request, "events/attendance.html", context)
