from django.views import generic
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, reverse
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.db.models import Q
from dal import autocomplete
from functools import wraps
from random import randint

from .models import OffChallenge, BitByteActivity, Announcement, CandidateForm
from ..events.models import Event, Rsvp
from .forms import ChallengeRequestForm, ChallengeConfirmationForm, BitByteRequestForm

# decorators

# first requires log in, but if you're already logged in but don't have permission, displays more info
def login_and_permission(permission_name):
    def decorator(func):
        return wraps(func)( # preserves function attributes to the decorated function
                login_required(login_url='/accounts/login/')(
                    # raises 403 error which invokes our custom 403.html
                    permission_required(permission_name, login_url='/accounts/login/', raise_exception=True)(
                        func # decorates function with both login_required and permission_required
                    )
                )
            )
    return decorator

def method_login_and_permission(permission_name):
    return method_decorator(login_and_permission(permission_name), name='dispatch')

# views

# Candidate portal home
@method_login_and_permission('candidate.view_announcement')
class IndexView(generic.TemplateView):
    template_name = 'candidate/index.html'
    context_object_name = 'my_favorite_publishers'

    def get_context_data(self):
        challenges = OffChallenge.objects \
                .filter(requester__exact=self.request.user)
        # if either one is waiting, challenge is still being reviewed
        num_pending = challenges \
                .filter(Q(officer_confirmed__isnull=True) | Q(csec_confirmed__isnull=True)) \
                .count()
        num_rejected = challenges \
                .filter(Q(officer_confirmed=False) | Q(csec_confirmed=False)) \
                .count()
        num_confirmed = challenges.count() - num_pending - num_rejected

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
        unconfirmed_events = sort_rsvps_into_events(rsvps.filter(confirmed=False))
        req_statuses = check_requirements(confirmed_events, num_confirmed, num_bitbytes)
        upcoming_events = Event.objects \
                .filter(start_time__range=(today, today + timezone.timedelta(days=7))) \
                .order_by('start_time')

        context = {
            'num_pending' : num_pending,
            'num_rejected' : num_rejected,
            # anything not pending or rejected is confirmed
            'num_confirmed' : num_confirmed,
            'num_bitbytes' : num_bitbytes,
            'announcements' : announcements,
            'confirmed_events': confirmed_events,
            'unconfirmed_events': unconfirmed_events,
            'req_statuses' : req_statuses,
            'upcoming_events': upcoming_events,
            'candidate_forms': candidate_forms,
        }
        return context

# Form for submitting officer challenge requests and list of past requests for candidate
@method_login_and_permission('candidate.add_offchallenge')
class CandRequestView(FormView, generic.ListView):
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
            'candidate/request_email.html',
            {
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

# List of past challenge requests for officer
# Non-officers can still visit this page by typing in the url,
# but it will not have any new entries
@method_login_and_permission('candidate.view_offchallenge')
class OffRequestView(generic.ListView):
    template_name = 'candidate/offreq.html'

    context_object_name = 'challenge_list'

    def get_queryset(self):
        result = OffChallenge.objects \
                .filter(officer__exact=self.request.user) \
                .order_by('-request_date')
        return result

# Form for submitting bit-byte activity requests and list of past requests for candidate
# Officers can still visit this page but it will not have any new entries
@method_login_and_permission('candidate.add_bitbyteactivity')
class BitByteView(FormView, generic.ListView):
    template_name = 'candidate/bitbyte.html'
    form_class = BitByteRequestForm
    success_url = "/cand/bitbyte"

    context_object_name = 'bitbyte_list'

    # resolve conflicting inheritance
    def get(self, request, *args, **kwargs):
        return generic.ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your request was submitted to the VP!')
        return super().form_valid(form)

    def get_queryset(self):
        result = BitByteActivity.objects \
                .filter(participants__exact=self.request.user) \
                .order_by('-request_date')
        return result

# Officer views and confirms a challenge request after clicking email link
# Only the officer who game the challenge can review it
@login_and_permission('candidate.change_offchallenge')
def officer_confirm_view(request, pk):
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
            send_cand_confirm_email(request, form.instance, True)
        # csec has not already rejected, and now officer rejects
        elif challenge.officer_confirmed is False and challenge.csec_confirmed is not False:
            send_cand_confirm_email(request, form.instance, False)
        # if neither is true, either need to wait for csec to review,
        # or csec has already rejected
        return redirect('/cand/reviewconfirm/{}'.format(pk))
    return render(request, "candidate/challenge_confirm.html", context=context)

# The page displayed after officer reviews challenge and clicks "submit"
@login_and_permission('candidate.view_offchallenge')
def officer_review_confirmation(request, pk):
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    context = {
        'challenge' : challenge,
        'requester_name' : requester_name,
    }
    return render(request, "candidate/review_confirm.html", context=context)

# Detail view of an officer challenge
@login_and_permission('candidate.view_offchallenge')
def challenge_detail_view(request, pk):
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

# HELPERS

# This function is not used; it can be used to view all photos available
def get_all_photos():
    with open(find("candidate/animal_photo_urls.txt")) as f:
        urls = f.readlines()
    return [url.strip() + "?w=400" for url in urls]

# images from pexels.com
def get_rand_photo(width=400):
    with open(find("candidate/animal_photo_urls.txt")) as f:
        urls = f.readlines()
    return urls[randint(0, len(urls) - 1)].strip() + "?w=" + str(width)

def send_cand_confirm_email(request, challenge, confirmed):
    subject = '[HKN] Your officer challenge was reviewed'
    candidate_email = challenge.requester.email

    challenge_link = request.build_absolute_uri(
            reverse("candidate:detail", kwargs={ 'pk': challenge.id }))
    html_content = render_to_string(
        'candidate/cand_confirm_email.html',
        {
            'confirmed': confirmed,
            'officer_name': challenge.officer.get_full_name(),
            'officer_username': challenge.officer.username,
            'challenge_link': challenge_link,
            'img_link': get_rand_photo(),
        }
    )
    msg = EmailMultiAlternatives(subject, subject,
            'no-reply@hkn.eecs.berkeley.edu', [candidate_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# what the event types are called on admin site
# code will not work if they're called something else!!
map_event_vars = {
    settings.MANDATORY_EVENT: 'Mandatory',
    settings.FUN_EVENT: 'Fun',
    settings.BIG_FUN_EVENT: 'Big Fun',
    settings.SERV_EVENT: 'Serv',
    settings.PRODEV_EVENT: 'Prodev',
    settings.HANGOUT_EVENT: 'Hangout',
}

# Takes in all confirmed rsvps and sorts them into types, current hard coded
# TODO: support more flexible typing and string-to-var parsing/conversion
def sort_rsvps_into_events(rsvps):
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    sorted_events = dict.fromkeys(map_event_vars.keys())
    for event_key, event_type in map_event_vars.items():
        temp = []
        for rsvp in rsvps.filter(event__event_type__type=event_type):
            temp.append(rsvp.event)
        sorted_events[event_key] = temp
    return sorted_events


# TODO: increase flexibility by fetching event requirement count from database
req_list = {
    settings.MANDATORY_EVENT: 3,
    settings.FUN_EVENT: 3,
    settings.BIG_FUN_EVENT: 1,
    settings.SERV_EVENT: 1,
    settings.PRODEV_EVENT: 1,
    settings.HANGOUT_EVENT: None,
    settings.BITBYTE_ACTIVITY: 3,
}

# Checks which requirements have been fulfilled by a candidate
def check_requirements(sorted_rsvps, num_challenges, num_bitbytes):
    req_statuses = dict.fromkeys(req_list.keys(), False)
    for req_type, minimum in req_list.items():
        if req_type == settings.BITBYTE_ACTIVITY:
            num_confirmed = num_bitbytes
        else:
            num_confirmed = len(sorted_rsvps[req_type])
        # officer hangouts are special case
        if req_type == settings.HANGOUT_EVENT:
            req_statuses[req_type] = check_interactivity_requirements(num_confirmed, num_challenges)
        elif num_confirmed >= minimum:
            req_statuses[req_type] = True
    return req_statuses

# returns whether officer interactivities are satisfied
def check_interactivity_requirements(hangouts, challenges):
    return hangouts >= 1 and challenges >= 1 and hangouts + challenges >= 3
