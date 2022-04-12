from typing import Tuple
import csv
import bleach

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic
from django.utils.safestring import mark_safe

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


NO_CHECKOFF_ACTION_TAKEN = """No checkoff action has been taken, so re-upload the entire file 
    after fixing the errors."""
INVALID_ENTRY_HEADER = """Invalid CSV format. Check that your columns are correctly labeled, there are 
            NO blank rows, and filled out for each row."""
INVALID_ENTRY_CONTENT = """Candidate error message: {}. --- Error Row Information 
    at row {}: {}"""
USER_ERROR_HEADER = """Could not find users listed. Please check that their 1) information is 
    correct and 2) they have an account."""
USER_ERROR_CONTENT = "{} {} --- with email {}."
CHECKOFF_TYPE_INFO = {
    "project": {
        "arg_name": "project_selection",
        "missing_arg_message": "Please select a valid committee project!",
        "model_cls": CommitteeProject,
        "model_done_cls": CommitteeProjectDoneEntry,
        "model_attr_name": "committeeProject",
    },
    "dues": {
        "arg_name": "dues_selection",
        "missing_arg_message": "Please input a valid Dues entry!",
        "model_cls": DuePayment,
        "model_done_cls": DuePaymentPaidEntry,
        "model_attr_name": "duePayment",
    },
    "forms": {
        "arg_name": "forms_selection",
        "missing_arg_message": "Please input a valid Forms entry!",
        "model_cls": CandidateForm,
        "model_done_cls": CandidateFormDoneEntry,
        "model_attr_name": "form",
    },
}


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
    if request.method != "POST":
        raise Http404()

    next_page = request.POST.get("next", "/")

    mem_csv = get_mem_csv(request)
    if not mem_csv:
        messages.error(request, "Please input a csv file!")
        return redirect(next_page)  # lgtm [py/url-redirection]

    users, error_html = get_users(mem_csv)
    if error_html:
        messages.error(request, error_html)
        return redirect(next_page)  # lgtm [py/url-redirection]

    checkoff_type = request.POST.get("checkoff_type", "")
    error = ""
    if checkoff_type == "event":
        error = checkoff_events(request, users)
    elif checkoff_type in CHECKOFF_TYPE_INFO:
        error = checkoff_requirement(request, CHECKOFF_TYPE_INFO[checkoff_type], users)
    else:
        error = "Invalid checkoff type"

    if error:
        messages.error(request, error)
    else:
        messages.success(request, "Successfully checked everyone off!")

    return redirect(next_page)  # lgtm [py/url-redirection]


def get_mem_csv(request) -> csv.DictReader:
    csv_file = request.FILES.get("csv_file", None)
    if not csv_file or not csv_file.name.endswith(ATTR.CSV_ENDING):
        return None

    decoded_csv_file = csv_file.read().decode(ATTR.UTF8SIG).splitlines()
    mem_csv = csv.DictReader(decoded_csv_file)

    return mem_csv


def get_users(mem_csv: csv.DictReader) -> Tuple[list, str]:
    # Pre-screen and validate data
    users, errors = [], []
    for i, row in enumerate(mem_csv):
        try:
            m = CandidateDTO(row)
        except AssertionError as e:
            errors.append(
                (INVALID_ENTRY_HEADER, INVALID_ENTRY_CONTENT.format(str(e), i + 1, row))
            )
            continue

        user = User.objects.filter(
            first_name=m.first_name, last_name=m.last_name, email=m.email
        ).first()
        if not user:
            errors.append(
                (
                    USER_ERROR_HEADER,
                    USER_ERROR_CONTENT.format(m.first_name, m.last_name, m.email),
                )
            )
            continue

        users.append(user)

    error_html = None
    if errors:
        error_html_elements = [
            f"<li>{e[0]}-{bleach.clean(e[1], tags=[])}</li>" for e in errors
        ]
        error_html = (
            f"{NO_CHECKOFF_ACTION_TAKEN}\n<ul>"
            + "".join(error_html_elements)
            + "</ul>\n"
        )
        error_html = mark_safe(error_html)

    return users, error_html


def checkoff_events(request, users: list) -> str:
    event = Event.objects.filter(pk=request.POST.get("event_id")).first()
    if not event:
        return "Please input a valid event ID!"

    for user in users:
        rsvp, _ = Rsvp.objects.get_or_create(event=event, user=user)
        rsvp.confirmed = True
        rsvp.save()

    return ""


def checkoff_requirement(request, info: dict, users: list) -> str:
    id = request.POST.get(info["arg_name"], None)
    if id is None:
        return info["missing_arg_message"]

    modelDoneEntry, _ = info["model_done_cls"].objects.get_or_create(
        **{info["model_attr_name"]: info["model_cls"].objects.get(id=id)}
    )

    for user in users:
        modelDoneEntry.users.add(user)

    return ""
