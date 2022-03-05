from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic

import csv

from hknweb.events.models import Event, Rsvp

from hknweb.candidate.constants import ATTR, CandidateDTO
from hknweb.candidate.models import (
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
)

from hknweb.utils import method_login_and_permission, login_and_permission


@method_login_and_permission("candidate.change_offchallenge")
class MemberCheckoffView(generic.TemplateView):
    """Form for submitting csv of members for mass checkoffs."""

    template_name = "candidate/checkoffs.html"

    context_object_name = "checkoff_context"

    def get_context_data(self):
        projects = CommitteeProject.objects.filter(visible=True).order_by("-duedate")
        dues = DuePayment.objects.filter(visible=True).order_by("-duedate")
        forms = CandidateForm.objects.filter(visible=True).order_by("-duedate")

        context = {"projects": projects, "dues": dues, "forms": forms}
        return context


@login_and_permission("candidate.change_offchallenge")
def checkoff_csv(request):
    if request.method != ATTR.POST:
        raise Http404()
    next_page = request.POST.get("next", "/")
    csv_file = request.FILES.get("csv_file", None)
    if not csv_file or not csv_file.name.endswith(ATTR.CSV_ENDING):
        messages.error(request, "Please input a csv file!")
        return redirect(next_page)
    decoded_csv_file = csv_file.read().decode(ATTR.UTF8SIG).splitlines()
    mem_csv = csv.DictReader(decoded_csv_file)

    checkoff_type = request.POST.get("checkoff_type", "")
    if checkoff_type == "event":
        event_id = request.POST.get("event_id", None)
        if event_id is None:
            messages.error(request, "Please input an event ID!")
            return redirect(next_page)
        event = Event.objects.filter(pk=event_id)
        if not event:
            messages.error(request, "Please input a valid event ID!")
            return redirect(next_page)
        event = event.first()
    elif checkoff_type == "project":
        project_id = request.POST.get("project_selection", None)
        if project_id is None:
            messages.error(request, "Please select a valid committee project!")
            return redirect(next_page)
        project = CommitteeProject.objects.get(id=project_id)
        projectDoneEntry = CommitteeProjectDoneEntry.objects.filter(
            committeeProject=project
        ).first()
        if projectDoneEntry is None:
            messages.error(
                request,
                "Could not find a corresponding CommiteeProjectDoneEntry. Please make sure one is created for the project.",
            )
            return redirect(next_page)
    elif checkoff_type == "dues":
        dues_id = request.POST.get("dues_selection", None)
        if dues_id is None:
            messages.error(request, "Please input a valid Dues entry!")
            return redirect(next_page)
        due = DuePayment.objects.get(id=dues_id)
        duesDoneEntry = DuePaymentPaidEntry.objects.filter(duePayment=due).first()
        if duesDoneEntry is None:
            messages.error(
                request,
                "Could not find a corresponding DuePaymentPaidEntry. Please make sure one is created for the due.",
            )
            return redirect(next_page)
    elif checkoff_type == "forms":
        forms_id = request.POST.get("forms_selection", None)
        if forms_id is None:
            messages.error(request, "Please input a valid Forms entry!")
            return redirect(next_page)
        form = CandidateForm.objects.get(id=forms_id)
        formsDoneEntry = CandidateFormDoneEntry.objects.filter(form=form).first()
        if formsDoneEntry is None:
            messages.error(
                request,
                "Could not find a corresponding CandidateFormDoneEntry. Please make sure one is created for the form.",
            )
            return redirect(next_page)
    else:
        messages.error(request, "Invalid checkoff type")
        return redirect(next_page)

    # Pre-screen and validate data
    users = []
    for i, row in enumerate(mem_csv):
        try:
            memberdto = CandidateDTO(row)
        except AssertionError as e:
            error_msg = "Invalid CSV format. Check that your columns are correctly labeled, there are NO blank rows, and filled out for each row."
            error_msg += " "
            error_msg += "No checkoff actions have been taken, so re-upload the entire file after fixing the errors."
            error_msg += " "
            error_msg += "Candidate error message: {}.".format(e)
            error_msg += " "
            error_msg += "Error Row Information at row {}: {}".format(i + 1, row)
            messages.error(request, error_msg)
            return redirect(next_page)
        user = User.objects.filter(
            first_name=memberdto.first_name,
            last_name=memberdto.last_name,
            email=memberdto.email,
        )
        if not user:
            messages.error(
                request,
                "Could not find user "
                + memberdto.first_name
                + " "
                + memberdto.last_name
                + " with email "
                + memberdto.email
                + ". Please check these parameters again. No checkoff action has been taken, so re-upload the entire file after fixing the errors.",
            )
            return redirect(next_page)
        users.append(user[0])

    # Checkoff all
    for user in users:
        if checkoff_type == "event":
            rsvp = Rsvp.objects.filter(event=event, user=user)
            if rsvp.count() != 0:
                rsvp = rsvp[0]
                rsvp.confirmed = True
            else:
                rsvp = Rsvp.objects.create(user=user, event=event, confirmed=True)
            rsvp.save()
        elif checkoff_type == "project":
            projectDoneEntry.users.add(user)
        elif checkoff_type == "dues":
            duesDoneEntry.users.add(user)
        elif checkoff_type == "forms":
            formsDoneEntry.users.add(user)

    messages.success(request, "Successfully checked everyone off!")

    return redirect(next_page)
