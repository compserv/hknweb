from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic
from django.utils.safestring import mark_safe

import csv
import bleach

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

NO_CHECKOFF_ACTION_TAKEN = "No checkoff action has been taken, so re-upload the entire file after fixing the errors."

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

class InvalidEntryErrorInfo:
    def __init__(self, error_msg, index, row_content):
        self.error_msg = error_msg
        self.index = index
        self.row_content = row_content
    
    @staticmethod
    def error_header():
        error_msg = "Invalid CSV format."
        error_msg += " "
        error_msg += "Check that your columns are correctly labeled, there are NO blank rows, and filled out for each row."
        return error_msg

    def __str__(self):
        error_msg = "Candidate error message: {}.".format(self.error_msg)
        error_msg += " --- "
        error_msg += "Error Row Information at row {}: {}".format(self.index, self.row_content)
        return error_msg

class UserErrorInfo:
    def __init__(self, memberdto):
        self.first_name = memberdto.first_name
        self.last_name = memberdto.last_name
        self.email = memberdto.email
    
    @staticmethod
    def error_header():
        error_msg = "Could not find users listed."
        error_msg += " "
        error_msg += "Please check that their 1) information is correct and 2) they have an account."
        return error_msg

    def __str__(self):
        return "{} {} --- with email {}.".format(self.first_name, self.last_name, self.email)

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
    invalid_csv_format_errors = []
    could_not_find_user_errors = []
    for i, row in enumerate(mem_csv):
        try:
            memberdto = CandidateDTO(row)
        except AssertionError as e:
            invalid_csv_format_errors.append(InvalidEntryErrorInfo(str(e), i + 1, row))
            continue
        user = User.objects.filter(
            first_name=memberdto.first_name,
            last_name=memberdto.last_name,
            email=memberdto.email,
        )
        if not user:
            could_not_find_user_errors.append(UserErrorInfo(memberdto))
            continue
        users.append(user[0])

    if invalid_csv_format_errors or could_not_find_user_errors:
        final_error_html = NO_CHECKOFF_ACTION_TAKEN + "\n<ul>\n"
        for errors in (invalid_csv_format_errors, could_not_find_user_errors):
            if errors:
                # The "if" says at least one, and only need the staticmethod
                error_html = "<li>" + errors[0].error_header() + "</li>" + "\n"
                error_html_elements = []
                for error in errors:
                    bleached_error = bleach.clean(str(error), tags=[])
                    error_html_elements.append(bleached_error)
                error_html += "<ul>\n"

                error_html += "<li>\n"
                error_html += "</li>\n<li>".join(error_html_elements)
                error_html += "</li>\n"

                error_html += "</ul>\n"

                final_error_html += error_html
        final_error_html += "</ul>\n"
        messages.error(request, mark_safe(final_error_html))
        return redirect(next_page)

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
