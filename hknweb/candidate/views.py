from django.views import generic
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.db.models import Q
from random import randint
import datetime

from .models import OffChallenge, Announcement
from ..events.models import Event, Rsvp
from .forms import ChallengeRequestForm, ChallengeConfirmationForm

# decorators

# used for things only officers and candidates can access
# TODO: use permissions instead of just the groups
def check_account_access(func):
    def check_then_call(request, *args, **kwargs):
        if not is_cand_or_officer(request.user):
            return render(request, "errors/401.html", status=401)
        return func(request, *args, **kwargs)
    return check_then_call


# views

# Candidate portal home
@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(check_account_access, name='dispatch')
# @method_decorator(is_cand_or_officer)
class IndexView(generic.TemplateView):
    template_name = 'candidate/index.html'
    context_object_name = 'my_favorite_publishers'

    def get_context_data(self):
        challenges = OffChallenge.objects \
                .filter(requester__exact=self.request.user) \
                .order_by('-request_date')
        # if either one is waiting, challenge is still being reviewed
        num_pending = challenges \
                .filter(Q(officer_confirmed__isnull=True) | Q(csec_confirmed__isnull=True)) \
                .count()
        num_rejected = challenges \
                .filter(Q(officer_confirmed=False) | Q(csec_confirmed=False)) \
                .count()

        announcements = Announcement.objects \
                .filter(visible=True) \
                .order_by('-release_date')

        today = datetime.date.today()
        rsvps = Rsvp.objects.filter(user__exact=self.request.user)
        # Both confirmed and unconfirmed rsvps have been sorted into event types
        confirmed_events = sort_rsvps_into_events(rsvps.filter(confirmed=True))
        unconfirmed_events = sort_rsvps_into_events(rsvps.filter(confirmed=False))
        req_statuses = check_requirements(confirmed_events)
        upcoming_events = Event.objects \
                .filter(start_time__range=(today, today + datetime.timedelta(days=7))) \
                .order_by('start_time')

        context = {
            'num_pending' : num_pending,
            'num_rejected' : num_rejected,
            # anything not pending or rejected is confirmed
            'num_confirmed' : challenges.count() - num_pending - num_rejected,
            'announcements' : announcements,
            'confirmed_events': confirmed_events,
            'unconfirmed_events': unconfirmed_events,
            'req_statuses' : req_statuses,
            'upcoming_events': upcoming_events,
        }
        return context


# Form for submitting officer challenge requests
# And list of past requests for candidate
@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(check_account_access, name='dispatch')
class CandRequestView(FormView, generic.ListView):
    template_name = 'candidate/candreq.html'
    form_class = ChallengeRequestForm
    success_url = "/cand/candreq"

    context_object_name = 'challenge_list'

    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.save()
        self.send_request_email(form)
        messages.success(self.request, 'Your request was submitted to the officer!')
        return super().form_valid(form)

    def send_request_email(self, form):
        subject = 'Confirm Officer Challenge'
        officer_email = form.instance.officer.email
        text_content = 'Confirm officer challenge'

        confirm_link = self.request.build_absolute_uri(
                reverse("candidate:challengeconfirm", kwargs={ 'pk' : form.instance.id }))
        html_content = render_to_string(
            'candidate/request_email.html',
            {
                'candidate_name' : form.instance.requester.get_full_name(),
                # TODO: for some usernames such as catherine.hu, this becomes a link. Why??
                'candidate_username' : form.instance.requester.username,
                'confirm_link' : confirm_link,
                'img_link' : get_rand_photo(),
            }
        )
        msg = EmailMultiAlternatives(subject, text_content,
                'no-reply@hkn.eecs.berkeley.edu', [officer_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_queryset(self):
        result = OffChallenge.objects \
                .filter(requester__exact=self.request.user) \
                .order_by('-request_date')
        return result


# List of past challenge requests for officer
# Non-officers can still visit this page but it will not have any entries
@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(check_account_access, name='dispatch')
class OffRequestView(generic.ListView):
    template_name = 'candidate/offreq.html'

    context_object_name = 'challenge_list'

    def get_queryset(self):
        result = OffChallenge.objects \
                .filter(officer__exact=self.request.user) \
                .order_by('-request_date')
        return result


# Officer views and confirms a challenge request after clicking email link
# Only the officer who game the challenge can review it
@login_required(login_url='/accounts/login/')
@check_account_access
def officer_confirm_view(request, pk):
    # TODO: gracefully handle when a challenge does not exist
    challenge = OffChallenge.objects.get(id=pk)
    if request.user.id != challenge.officer.id:
        return render(request, "errors/401.html", status=401)

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
        if challenge.officer_confirmed is True and challenge.csec_confirmed is True:
            send_cand_confirm_email(request, form.instance, True)
        elif challenge.officer_confirmed is False:
            send_cand_confirm_email(request, form.instance, False)
        # if neither is true, need to wait for csec to review before sending email
        return redirect('/cand/reviewconfirm/{}'.format(pk))
    return render(request, "candidate/challenge_confirm.html", context=context)


# The page displayed after officer reviews challenge and clicks "submit"
@login_required(login_url='/accounts/login/')
@check_account_access
def officer_review_confirmation(request, pk):
    challenge = OffChallenge.objects.get(id=pk)
    requester_name = challenge.requester.get_full_name()
    context = {
        'challenge' : challenge,
        'requester_name' : requester_name,
    }
    return render(request, "candidate/review_confirm.html", context=context)


# Detail view of an officer challenge
@login_required(login_url='/accounts/login/')
@check_account_access
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


# HELPERS

def is_cand_or_officer(user):
    return user.groups.filter(name=settings.CAND_GROUP).exists() or \
            user.groups.filter(name=settings.OFFICER_GROUP).exists()

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
    subject = 'Your Officer Challenge Was Reviewed'
    candidate_email = challenge.requester.email
    text_content = 'Your Officer Challenge Was Reviewed'

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
    msg = EmailMultiAlternatives(subject, text_content,
            'no-reply@hkn.eecs.berkeley.edu', [candidate_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Takes in all confirmed rsvps and sorts them into types, current hard coded
# TODO: support more flexible typing and string-to-var parsing/conversion 
def sort_rsvps_into_events(rsvps):
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    map_event_vars = {
        'mandatory_meetings': 'Mandatory', 
        'big_fun': 'Big Fun', 
        'fun': 'Fun',
        'serv': 'Serv',
        'prodev': 'Prodev',
    }
    sorted_events = dict.fromkeys(map_event_vars.keys())
    for event_key, event_type in map_event_vars.items():
        temp = []
        for rsvp in rsvps.filter(event__event_type__type=event_type):
            temp.append(rsvp.event)
        sorted_events[event_key] = temp
    return sorted_events

# Checks which requirements have been fulfilled by a candidate
def check_requirements(sorted_rsvps):
    # TODO: increase flexibility by fetching event requirement count from database
    req_list = {
        'mandatory_meetings': 3, 
        'big_fun': 1,
        'fun': 3,
        'serv': 1,
        'prodev': 1,
    }
    req_statuses = dict.fromkeys(req_list.keys(), False)
    for req_type, minimum in req_list.items():
        if len(sorted_rsvps[req_type])>= minimum:
            req_statuses[req_type] = True
    return req_statuses

