from django.shortcuts import render, redirect
from django.contrib import messages

from hknweb.utils import login_and_permission
from hknweb.events.models import AttendanceForm
from hknweb.events.forms import AttendanceFormForm, AttendanceResponseForm


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
        else:
            messages.error(request, form.errors)

    return render(request, "events/attendance_manage.html", {"form": form})


@login_and_permission("events.change_rsvp")
def submit_attendance(request, event_id, attendance_form_id, rsvp_id):
    form = AttendanceResponseForm(request.POST or None)
    if request.method == "POST":
        form.data = form.data.copy()
        form.data["attendance_form"] = attendance_form_id
        form.data["rsvp"] = rsvp_id

        if form.is_valid():
            if form.data["secret_word"] == AttendanceForm.objects.get(pk=attendance_form_id).secret_word:
                form.save()
                messages.success(request, "RSVP confirmed!")
                return redirect("events:detail", id=event_id)
            else:
                messages.error(request, "Secret word is incorrect!")
        else:
            messages.error(request, form.errors)

    return render(request, "events/attendance_submit.html", {"form": form})
