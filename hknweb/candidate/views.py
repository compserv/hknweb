from collections import OrderedDict
import csv
from typing import Tuple

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import BaseUserManager, Group, User
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView

from dal import autocomplete
from multiprocessing import Pool
from hknweb.models import Profile
from hknweb.views.users import get_current_cand_semester
from hknweb.utils import get_access_level, GROUP_TO_ACCESSLEVEL

from hknweb.utils import (
    get_rand_photo,
    login_and_permission,
    method_login_and_permission,
)

from ..events.models import Event, Rsvp

from .constants import ATTR, DEFAULT_RANDOM_PASSWORD_LENGTH, CandidateDTO
from .forms import BitByteRequestForm, ChallengeConfirmationForm, ChallengeRequestForm
from .models import (
    BitByteActivity,
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
    OffChallenge,
)
from .utils import send_challenge_confirm_email
from .utils_candportal import CandidatePortalData

@method_login_and_permission("candidate.view_announcement")
class IndexView(generic.TemplateView):
    """Candidate portal home."""

    template_name = "candidate/index.html"
    context_object_name = "my_favorite_publishers"

    def get_context_data(self):
        cand_data = CandidatePortalData(self.request.user)
        return cand_data.get_user_cand_data()

@login_required
def candidate_portal_view_by_username(request, username):
    if GROUP_TO_ACCESSLEVEL["member"] < get_access_level(request.user):
        messages.warning(request, "Insufficent permission to access a user.")
        return HttpResponseRedirect("/")
    
    user = User.objects.filter(username=username).first()
    if user is None:
        messages.warning(request, "User {} does not exist.".format(username))
        return HttpResponseRedirect(reverse("candidate:index"))
    cand_data = CandidatePortalData(user)
    user_cand_data = cand_data.get_user_cand_data()
    user_cand_data["user_self"] = False
    return render(request, "candidate/index.html", context=user_cand_data)

@method_login_and_permission("candidate.add_offchallenge")
class CandRequestView(FormView, generic.ListView):
    """Form for submitting officer challenge requests and list of past requests for candidate."""

    template_name = "candidate/candreq.html"
    form_class = ChallengeRequestForm
    success_url = "/cand/candreq"

    context_object_name = "challenge_list"

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.save()
        self.send_request_email(form)
        messages.success(self.request, "Your request was submitted to the officer!")
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = "[HKN] Confirm Officer Challenge"
        officer_email = form.instance.officer.email

        confirm_link = self.request.build_absolute_uri(
            reverse("candidate:challengeconfirm", kwargs={"pk": form.instance.id})
        )
        html_content = render_to_string(
            "candidate/challenge_request_email.html",
            {
                "subject": subject,
                "candidate_name": form.instance.requester.get_full_name(),
                "candidate_username": form.instance.requester.username,
                "confirm_link": confirm_link,
                "img_link": get_rand_photo(),
            },
        )
        msg = EmailMultiAlternatives(
            subject, subject, settings.NO_REPLY_EMAIL, [officer_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = OffChallenge.objects.filter(
            requester__exact=self.request.user
        ).order_by("-request_date")
        return result


@method_login_and_permission("candidate.view_offchallenge")
class OfficerPortalView(generic.ListView):
    """Officer portal.
    List of past challenge requests for officer.
    Non-officers can still visit this page by typing in the url,
    but it will not have any new entries. Option to add
    new candidates."""

    template_name = "candidate/officer_portal.html"

    context_object_name = "challenge_list"

    def get_queryset(self):
        result = OffChallenge.objects.filter(officer__exact=self.request.user).order_by(
            "-request_date"
        )
        return result

def check_duplicates(candidatedto: CandidateDTO, row: OrderedDict,
                     email_set: set, username_set: set, i: int) -> Tuple[bool, str]:
    error_msg = ""
    # Check for duplicate Email
    cand_email_in_set = candidatedto.email in email_set
    if (cand_email_in_set or User.objects.filter(email=candidatedto.email).count() > 0):
        if cand_email_in_set:
            error_msg = "Duplicate email {} in the Candidate data.".format(candidatedto.email)
        else:
            error_msg = "Account with email {} already exists.".format(candidatedto.email)
        error_msg += " "
        error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
        error_msg += " "
        error_msg += "Error Row Information at row {}: {}.".format(i + 1, row)
        return True, error_msg
    # Check for duplicate Username
    cand_username_in_set = candidatedto.username in username_set
    if (cand_username_in_set or User.objects.filter(username=candidatedto.username).count() > 0):
        if cand_username_in_set:
            error_msg = "Duplicate username {} in the Candidate data.".format(candidatedto.username)
        else:
            error_msg = "Account of username {} already exists.".format(candidatedto.username)
        error_msg += " "
        error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
        error_msg += " "
        error_msg += "Error Row Information at row {}: {}.".format(i + 1, row)
        return True, error_msg
    return False, ""

@login_and_permission("auth.add_user")
def add_cands(request):
    if request.method != ATTR.POST:
        raise Http404()
    next_page = request.POST.get(ATTR.NEXT, "/")

    cand_csv_file = request.FILES.get(ATTR.CAND_CSV, None)
    if not cand_csv_file.name.endswith(ATTR.CSV_ENDING):
        messages.error(request, "Please input a csv file!")
    decoded_cand_csv_file = cand_csv_file.read().decode(ATTR.UTF8SIG).splitlines()
    cand_csv = csv.DictReader(decoded_cand_csv_file)

    candidate_group = Group.objects.get(name=ATTR.CANDIDATE)

    # Pre-screen and validate data
    new_cand_list = []
    email_set = set()
    username_set = set()
    current_cand_semester = get_current_cand_semester()
    email_passwords = {}
    if current_cand_semester is None:
        error_msg = "Inform CompServ the following: Please add the current semester in CourseSemester."
        error_msg += " "
        error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
        messages.error(request, error_msg)
        return redirect(next_page)
    for i, row in enumerate(cand_csv):
        if i >= 30:
            error_msg = "Preprocessing stopped! Detected more than 30 account requests!"
            error_msg += " "
            error_msg += "Please upload the file in separate batches of 30 account requests each."
            error_msg += " "
            error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
            messages.error(request, error_msg)
            return redirect(next_page)
        try:
            candidatedto = CandidateDTO(row)
        except AssertionError as e:
            error_msg = "Invalid CSV format. Check that your columns are correctly labeled, there are NO blank rows, and filled out for each row."
            error_msg += " "
            error_msg += "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."
            error_msg += " "
            error_msg += "Candidate error message: {}.".format(e)
            error_msg += " "
            error_msg += "Row Information at row {}: {}.".format(i + 1, row)
            messages.error(request, error_msg)
            return redirect(next_page)

        password = BaseUserManager.make_random_password(
            None, length=DEFAULT_RANDOM_PASSWORD_LENGTH
        )
        
        duplicate, error_msg = check_duplicates(candidatedto, row, email_set, username_set, i)
        if duplicate:
            messages.error(request, error_msg)
            return redirect(next_page)
        
        new_cand = User(
            username=candidatedto.username,
            email=candidatedto.email,
        )
        email_set.add(candidatedto.email)
        username_set.add(candidatedto.username)
        new_cand.first_name = candidatedto.first_name
        new_cand.last_name = candidatedto.last_name
        new_cand.set_password(password)
        new_cand_list.append(new_cand)
        email_passwords[new_cand.email] = password
    
    # Release the memory once done
    del email_set
    del username_set
    
    # Add all candidates
    count = 0
    email_pool = Pool(processes=4)
    # This should be capped at 4, since Gmail doesn't like lots
    #  of emails being sent in succession
    # If there's a 421 Temp Error from the Mailing Service, adjust this number down
    email_pool_list = []
    for new_cand in new_cand_list:
        new_cand.save()
        candidate_group.user_set.add(new_cand)

        profile = Profile.objects.get(user=new_cand)
        profile.candidate_semester = current_cand_semester
        profile.save()

        subject = "[HKN] Candidate account"
        html_content = render_to_string(
            "candidate/new_candidate_account_email.html",
            {
                "subject": subject,
                "first_name": new_cand.first_name,
                "username": new_cand.username,
                "password": email_passwords[new_cand.email],
                "website_link": request.build_absolute_uri("/accounts/login/"),
                "img_link": get_rand_photo(),
            },
        )
        msg = EmailMultiAlternatives(
            subject, subject, settings.NO_REPLY_EMAIL, [new_cand.email]
        )
        msg.attach_alternative(html_content, "text/html")
        email_pool_list.append(email_pool.apply_async(msg.send, args=()))
        count += 1
    email_pool.close()
    
    email_errors = []
    i = 0
    while i < len(email_pool_list):
        try:
            while i < len(email_pool_list):
                p = email_pool_list[i]
                p.get()
                i += 1
        except Exception as e:
            email_errors.append((new_cand_list[i].email, str(e)))
            i += 1
    
    # If gone through everything and no errors
    if len(email_errors) > 0:
        messages.warning(request, "An error occured during the sending of emails. "
                                + "Candidate Email and Error Messages: " + str(email_errors) + " --- "
                                + "Inform CompServ of the errors, and inform the candidates "
                                + "to access their accounts by resetting their password "
                                + "using \"Forget your password?\" in the Login page. "
                                + "All {} candidates added!".format(count))
    else:
        messages.success(request, "Successfully added {} candidates!".format(count))

    return redirect(next_page)


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
        event_id = request.POST.get("event_id", "")
        if not event_id:
            messages.error(request, "Please input an event ID!")
            return redirect(next_page)
        event = Event.objects.filter(pk=event_id)
        if not event:
            messages.error(request, "Please input a valid event ID!")
            return redirect(next_page)
        event = event[0]
    elif checkoff_type == "project":
        project_name = request.POST.get("project_name", "")
        project = CommitteeProject.objects.get(name=project_name)
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
        dues_name = request.POST.get("dues_name", "")
        due = DuePayment.objects.get(name=dues_name)
        duesDoneEntry = DuePaymentPaidEntry.objects.filter(duePayment=due).first()
        if duesDoneEntry is None:
            messages.error(
                request,
                "Could not find a corresponding DuePaymentPaidEntry. Please make sure one is created for the due.",
            )
            return redirect(next_page)
    elif checkoff_type == "forms":
        forms_name = request.POST.get("forms_name", "")
        form = CandidateForm.objects.get(name=forms_name)
        formsDoneEntry = CandidateFormDoneEntry.objects.filter(form=form).first()
        if formsDoneEntry is None:
            messages.error(
                request,
                "Could not find a corresponding CandidateFormDoneEntry. Please make sure one is created for the form.",
            )
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


@method_login_and_permission("candidate.add_bitbyteactivity")
class BitByteView(FormView, generic.ListView):
    """Form for submitting bit-byte activity requests and list of past requests for candidate.
    Officers can still visit this page, but it will not have any new entries."""

    template_name = "candidate/bitbyte.html"
    form_class = BitByteRequestForm
    success_url = "/cand/bitbyte"

    context_object_name = "bitbyte_list"

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.send_request_email(form)
        messages.success(self.request, "Your request was submitted to the VP!")
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = "[HKN] Bit-byte request submitted"
        participant_emails = [part.email for part in form.instance.participants.all()]

        bitbyte_link = self.request.build_absolute_uri(reverse("candidate:bitbyte"))
        html_content = render_to_string(
            "candidate/bitbyte_request_email.html",
            {
                "subject": subject,
                "requester": self.request.user,
                "participants": form.instance.participants.all(),
                "bitbyte_link": bitbyte_link,
                "img_link": get_rand_photo(),
            },
        )
        msg = EmailMultiAlternatives(
            subject, subject, settings.NO_REPLY_EMAIL, participant_emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = BitByteActivity.objects.filter(
            participants__exact=self.request.user
        ).order_by("-request_date")
        return result


@login_and_permission("candidate.change_offchallenge")
def officer_confirm_view(request, pk):
    """Officer views and confirms a challenge request after clicking email link.
    Only the officer who gave the challenge can review it."""
    challenge = OffChallenge.objects.get(id=pk)
    if request.user.id != challenge.officer.id:
        raise PermissionDenied  # not the officer that gave the challenge

    requester_name = challenge.requester.get_full_name()
    form = ChallengeConfirmationForm(request.POST or None, instance=challenge)
    context = {
        "challenge": challenge,
        "requester_name": requester_name,
        "form": form,
    }

    if form.is_valid():
        form.instance.reviewed = True
        form.save()
        # csec has already confirmed, and now officer confirms
        if challenge.officer_confirmed is True and challenge.csec_confirmed is True:
            send_challenge_confirm_email(request, form.instance, True)
        # csec has not already rejected, and now officer rejects
        elif (
            challenge.officer_confirmed is False
            and challenge.csec_confirmed is not False
        ):
            send_challenge_confirm_email(request, form.instance, False)
        # if neither is true, either need to wait for csec to review,
        # or csec has already rejected
        return redirect("/cand/reviewconfirm/{}".format(pk))
    return render(request, "candidate/challenge_confirm.html", context=context)


@login_and_permission("candidate.change_offchallenge")
def confirm_challenge(request, id):
    if request.method != "POST":
        raise Http404()

    offchallenge = get_object_or_404(OffChallenge, id=id)
    offchallenge.officer_confirmed = True
    offchallenge.save()

    next_page = request.POST.get("next", "/")
    return redirect(next_page)


@login_and_permission("candidate.view_offchallenge")
def officer_review_confirmation(request, pk):
    """The page displayed after officer reviews challenge and clicks "submit." """
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    context = {
        "challenge": challenge,
        "requester_name": requester_name,
    }
    return render(request, "candidate/review_confirm.html", context=context)


@login_and_permission("candidate.view_offchallenge")
def challenge_detail_view(request, pk):
    """Detail view of an officer challenge."""
    challenge = OffChallenge.objects.get(id=pk)
    officer_name = challenge.officer.get_full_name()
    requester_name = challenge.requester.get_full_name()

    # check whether the viewer of page is the officer who gave the challenge
    viewer_is_the_officer = challenge.officer == request.user
    # check whether the viewer of page is an officer
    if viewer_is_the_officer:
        review_link = request.build_absolute_uri(
            reverse("candidate:challengeconfirm", kwargs={"pk": pk})
        )
    else:
        review_link = None
    context = {
        "challenge": challenge,
        "officer_name": officer_name,
        "requester_name": requester_name,
        "viewer_is_the_officer": viewer_is_the_officer,
        # viewer_is_an_officer is already added as a context variable with a context processor
        "review_link": review_link,
    }
    return render(request, "candidate/challenge_detail.html", context=context)


# this is needed otherwise anyone can see the users in the database
@method_login_and_permission("auth.view_user")
class OfficerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(groups__name=settings.OFFICER_GROUP)
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )
        return qs


# this is needed otherwise anyone can see the users in the database
@method_login_and_permission("auth.view_user")
class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )
        return qs
