from django.shortcuts import render, redirect
from django.contrib import messages

from hknweb.utils import login_and_permission
from hknweb.events.models import AttendanceForm
from hknweb.events.forms import AttendanceResponseForm


@login_and_permission("events.change_rsvp")
def submit_attendance(request, event_id, attendance_form_id, rsvp_id):
    attendance_form = AttendanceForm.objects.get(pk=attendance_form_id)

    form = AttendanceResponseForm(request.POST or None)
    if request.method == "POST":
        form.data = form.data.copy()
        form.data["attendance_form"] = attendance_form_id
        form.data["rsvp"] = rsvp_id

        if form.is_valid():
            if form.data["secret_word"].lower() == attendance_form.secret_word.lower():
                form.save()
                messages.success(request, "RSVP confirmed!")
                return redirect("events:detail", id=event_id)
            else:
                messages.error(request, "Secret word is incorrect!")
        else:
            messages.error(request, form.errors)

    context = {
        "form": form,
        "description": attendance_form.description,
    }
    return render(request, "events/attendance.html", context)
