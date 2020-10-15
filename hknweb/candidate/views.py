import csv

from django.conf import settings

from django.contrib import messages
from django.contrib.auth.models import BaseUserManager, Group, User

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import PermissionDenied

from django.db.models import Q

from django.http import Http404

from django.shortcuts import get_object_or_404, redirect, render, reverse

from django.template.loader import render_to_string

from django.utils import timezone

from django.views import generic
from django.views.generic.edit import FormView

from dal import autocomplete

from hknweb.utils import get_rand_photo, login_and_permission, method_login_and_permission

from ..events.models import Event, Rsvp

from .constants import ATTR, DEFAULT_RANDOM_PASSWORD_LENGTH, REQUIREMENT_EVENTS, CandidateDTO
from .forms import BitByteRequestForm, ChallengeConfirmationForm, ChallengeRequestForm
from .models import Announcement, BitByteActivity, CandidateForm, OffChallenge
from .utils import (
    check_interactivity_requirements,
    check_requirements,
    create_title,
    get_requirement_colors,
    get_unconfirmed_events,
    req_list,
    send_bitbyte_confirm_email,
    send_challenge_confirm_email,
    sort_rsvps_into_events,
)


@method_login_and_permission('candidate.view_announcement')
class IndexView(generic.TemplateView):
    """ Candidate portal home. """
    template_name = 'candidate/index.html'
    context_object_name = 'my_favorite_publishers'

    def get_context_data(self):
        challenges = OffChallenge.objects \
                .filter(requester__exact=self.request.user)
        # if either one is waiting, challenge is still being reviewed
        num_confirmed = challenges \
                .filter(Q(officer_confirmed=True) & Q(csec_confirmed=True)) \
                .count()
        num_rejected = challenges \
                .filter(Q(officer_confirmed=False) | Q(csec_confirmed=False)) \
                .count()
        num_pending = challenges.count() - num_confirmed - num_rejected

        num_bitbytes = BitByteActivity.objects \
                .filter(participants__exact=self.request.user) \
                .filter(confirmed=True) \
                .count()

        announcements = Announcement.objects \
                .filter(visible=True) \
                .order_by('-release_date')

        candidate_forms = CandidateForm.objects \
                .filter(visible=True) \
                .order_by('duedate')

        today = timezone.now()
        rsvps = Rsvp.objects.filter(user__exact=self.request.user)
        # Both confirmed and unconfirmed rsvps have been sorted into event types
        confirmed_events = sort_rsvps_into_events(rsvps.filter(confirmed=True))
        unconfirmed_events = get_unconfirmed_events(rsvps, today)
        req_statuses, req_remaining = check_requirements(confirmed_events, unconfirmed_events, num_confirmed, num_bitbytes)
        upcoming_events = Event.objects \
                .filter(start_time__range=(today, today + timezone.timedelta(days=7))) \
                .order_by('start_time')

        req_colors = get_requirement_colors()
        req_titles = {req_type: create_title(req_type, req_remaining) for req_type in req_statuses}

        events = []
        for req_event in REQUIREMENT_EVENTS:
            events.append({
                ATTR.TITLE: req_titles[req_event],
                ATTR.STATUS: req_statuses[req_event],
                ATTR.COLOR: req_colors[req_event],
                ATTR.CONFIRMED: confirmed_events[req_event],
                ATTR.UNCONFIRMED: unconfirmed_events[req_event],
            })

        interactivities = {
            ATTR.TITLE: req_titles[settings.HANGOUT_EVENT][settings.EITHER_ATTRIBUTE_NAME],
            ATTR.STATUS: req_statuses[settings.HANGOUT_EVENT],
            settings.CHALLENGE_ATTRIBUTE_NAME: {
                ATTR.TITLE: req_titles[settings.HANGOUT_EVENT][settings.CHALLENGE_ATTRIBUTE_NAME],
                ATTR.NUM_PENDING : num_pending,
                ATTR.NUM_REJECTED : num_rejected,
                # anything not pending or rejected is confirmed
                ATTR.NUM_CONFIRMED : num_confirmed,
            },
            settings.HANGOUT_ATTRIBUTE_NAME: {
                ATTR.TITLE: req_titles[settings.HANGOUT_EVENT][settings.HANGOUT_ATTRIBUTE_NAME],
            },
        }

        bitbyte = {
            ATTR.TITLE: req_titles[settings.BITBYTE_ACTIVITY],
            ATTR.STATUS: req_statuses[settings.BITBYTE_ACTIVITY],
            ATTR.NUM_BITBYTES : num_bitbytes,
        }

        context = {
            'announcements' : announcements,
            'confirmed_events': confirmed_events,
            'unconfirmed_events': unconfirmed_events,
            'req_statuses' : req_statuses,
            'upcoming_events': upcoming_events,
            'candidate_forms': candidate_forms,
            settings.EVENTS_ATTRIBUTE_NAME: events,
            settings.INTERACTIVITIES_ATTRIBUTE_NAME: interactivities,
            settings.BITBYTE_ACTIVITY: bitbyte,
        }
        return context

@method_login_and_permission('candidate.add_offchallenge')
class CandRequestView(FormView, generic.ListView):
    """ Form for submitting officer challenge requests and list of past requests for candidate. """
    template_name = 'candidate/candreq.html'
    form_class = ChallengeRequestForm
    success_url = "/cand/candreq"

    context_object_name = 'challenge_list'

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.save()
        self.send_request_email(form)
        messages.success(self.request, 'Your request was submitted to the officer!')
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = '[HKN] Confirm Officer Challenge'
        officer_email = form.instance.officer.email

        confirm_link = self.request.build_absolute_uri(
                reverse("candidate:challengeconfirm", kwargs={ 'pk' : form.instance.id }))
        html_content = render_to_string(
            'candidate/challenge_request_email.html',
            {
                'subject': subject,
                'candidate_name' : form.instance.requester.get_full_name(),
                'candidate_username' : form.instance.requester.username,
                'confirm_link' : confirm_link,
                'img_link' : get_rand_photo(),
            }
        )
        msg = EmailMultiAlternatives(subject, subject,
                'no-reply@hkn.eecs.berkeley.edu', [officer_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = OffChallenge.objects \
                .filter(requester__exact=self.request.user) \
                .order_by('-request_date')
        return result

@method_login_and_permission('candidate.view_offchallenge')
class OfficerPortalView(generic.ListView):
    """ Officer portal.
        List of past challenge requests for officer.
        Non-officers can still visit this page by typing in the url,
        but it will not have any new entries. Option to add
        new candidates. """
    template_name = 'candidate/officer_portal.html'

    context_object_name = 'challenge_list'

    def get_queryset(self):
        result = OffChallenge.objects \
                .filter(officer__exact=self.request.user) \
                .order_by('-request_date')
        return result

@login_and_permission("auth.add_user")
def add_cands(request):
    if request.method != ATTR.POST:
        raise Http404()
    next_page = request.POST.get(ATTR.NEXT, '/')

    cand_csv_file = request.FILES.get(ATTR.CAND_CSV, None)
    if not cand_csv_file.name.endswith(ATTR.CSV_ENDING):
        messages.error(request, "Please input a csv file!")
    decoded_cand_csv_file = cand_csv_file.read().decode(ATTR.UTF8).splitlines()
    cand_csv = csv.DictReader(decoded_cand_csv_file)

    candidate_group = Group.objects.get(name=ATTR.CANDIDATE)

    for row in cand_csv:
        try:
            candidatedto = CandidateDTO(row)
        except AssertionError as e:
            messages.error(request, "Invalid candidate information: " + str(e))
            return redirect(next_page)

        password = BaseUserManager.make_random_password(None, length=DEFAULT_RANDOM_PASSWORD_LENGTH)
        new_cand = User.objects.create_user(
            candidatedto.username,
            email=candidatedto.email,
            password=password,
        )
        new_cand.first_name = candidatedto.first_name
        new_cand.last_name = candidatedto.last_name
        new_cand.save()
        candidate_group.user_set.add(new_cand)

        subject = "[HKN] Candidate account"
        html_content = render_to_string(
            "candidate/new_candidate_account_email.html",
            {
                "subject": subject,
                "first_name": candidatedto.first_name,
                "username": candidatedto.username,
                "password": password,
                "website_link": request.build_absolute_uri("/accounts/login/"),
                "img_link": get_rand_photo(),
            }
        )
        msg = EmailMultiAlternatives(subject, subject,
                "no-reply@hkn.eecs.berkeley.edu", [candidatedto.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    messages.success(request, "Successfully added candidates!")

    return redirect(next_page)

@method_login_and_permission('candidate.add_bitbyteactivity')
class BitByteView(FormView, generic.ListView):
    """ Form for submitting bit-byte activity requests and list of past requests for candidate.
        Officers can still visit this page, but it will not have any new entries. """
    template_name = 'candidate/bitbyte.html'
    form_class = BitByteRequestForm
    success_url = "/cand/bitbyte"

    context_object_name = 'bitbyte_list'

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.send_request_email(form)
        messages.success(self.request, 'Your request was submitted to the VP!')
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = '[HKN] Bit-byte request submitted'
        participant_emails = [part.email for part in form.instance.participants.all()]

        bitbyte_link = self.request.build_absolute_uri(
            reverse("candidate:bitbyte"))
        html_content = render_to_string(
            'candidate/bitbyte_request_email.html',
            {
                'subject': subject,
                'requester': self.request.user,
                'participants': form.instance.participants.all(),
                'bitbyte_link': bitbyte_link,
                'img_link': get_rand_photo(),
            }
        )
        msg = EmailMultiAlternatives(subject, subject,
                    settings.NO_REPLY_EMAIL, participant_emails)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = BitByteActivity.objects \
                .filter(participants__exact=self.request.user) \
                .order_by('-request_date')
        return result

@login_and_permission('candidate.change_offchallenge')
def officer_confirm_view(request, pk):
    """ Officer views and confirms a challenge request after clicking email link.
        Only the officer who gave the challenge can review it. """
    challenge = OffChallenge.objects.get(id=pk)
    if request.user.id != challenge.officer.id:
        raise PermissionDenied # not the officer that gave the challenge

    requester_name = challenge.requester.get_full_name()
    form = ChallengeConfirmationForm(request.POST or None, instance=challenge)
    context = {
        'challenge': challenge,
        'requester_name': requester_name,
        'form': form,
    }

    if form.is_valid():
        form.instance.reviewed = True
        form.save()
        # csec has already confirmed, and now officer confirms
        if challenge.officer_confirmed is True and challenge.csec_confirmed is True:
            send_challenge_confirm_email(request, form.instance, True)
        # csec has not already rejected, and now officer rejects
        elif challenge.officer_confirmed is False and challenge.csec_confirmed is not False:
            send_challenge_confirm_email(request, form.instance, False)
        # if neither is true, either need to wait for csec to review,
        # or csec has already rejected
        return redirect('/cand/reviewconfirm/{}'.format(pk))
    return render(request, "candidate/challenge_confirm.html", context=context)

@login_and_permission('candidate.change_offchallenge')
def confirm_challenge(request, id):
    if request.method != 'POST':
        raise Http404()

    offchallenge = get_object_or_404(OffChallenge, id=id)
    offchallenge.officer_confirmed = True
    offchallenge.save()

    next_page = request.POST.get('next', '/')
    return redirect(next_page)

@login_and_permission('candidate.view_offchallenge')
def officer_review_confirmation(request, pk):
    """ The page displayed after officer reviews challenge and clicks "submit." """
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    context = {
        'challenge' : challenge,
        'requester_name' : requester_name,
    }
    return render(request, "candidate/review_confirm.html", context=context)

@login_and_permission('candidate.view_offchallenge')
def challenge_detail_view(request, pk):
    """ Detail view of an officer challenge. """
    challenge = OffChallenge.objects.get(id=pk)
    officer_name = challenge.officer.get_full_name()
    requester_name = challenge.requester.get_full_name()

    # check whether the viewer of page is the officer who gave the challenge
    viewer_is_the_officer = challenge.officer == request.user
    # check whether the viewer of page is an officer
    if viewer_is_the_officer:
        review_link = request.build_absolute_uri(
                reverse("candidate:challengeconfirm", kwargs={ 'pk' : pk }))
    else:
        review_link = None
    context = {
        "challenge" : challenge,
        "officer_name" : officer_name,
        "requester_name" : requester_name,
        "viewer_is_the_officer" : viewer_is_the_officer,
        # viewer_is_an_officer is already added as a context variable with a context processor
        "review_link" : review_link,
    }
    return render(request, "candidate/challenge_detail.html", context=context)

# this is needed otherwise anyone can see the users in the database
@method_login_and_permission('auth.view_user')
class OfficerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(groups__name=settings.OFFICER_GROUP)
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q) |
                Q(first_name__icontains=self.q) |
                Q(last_name__icontains=self.q))
        return qs

# this is needed otherwise anyone can see the users in the database
@method_login_and_permission('auth.view_user')
class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q) |
                Q(first_name__icontains=self.q) |
                Q(last_name__icontains=self.q))
        return qs
