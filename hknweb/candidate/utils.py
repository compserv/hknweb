from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import render_to_string

from hknweb.utils import get_rand_photo, get_semester_bounds

from ..events.models import Event, EventType

from .constants import REQUIREMENT_TITLES_TEMPLATE, REQUIREMENT_TITLES_MANDATORY


def send_challenge_confirm_email(request, challenge, confirmed):
    subject = '[HKN] Your officer challenge was reviewed'
    candidate_email = challenge.requester.email

    challenge_link = request.build_absolute_uri(
            reverse("candidate:detail", kwargs={ 'pk': challenge.id }))
    html_content = render_to_string(
        'candidate/challenge_confirm_email.html',
        {
            'subject': subject,
            'confirmed': confirmed,
            'officer_name': challenge.officer.get_full_name(),
            'officer_username': challenge.officer.username,
            'challenge_link': challenge_link,
            'img_link': get_rand_photo(),
        }
    )
    msg = EmailMultiAlternatives(subject, subject,
                settings.NO_REPLY_EMAIL, [candidate_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_bitbyte_confirm_email(request, bitbyte, confirmed):
    subject = '[HKN] Your bit-byte request was reviewed'
    participant_emails = [part.email for part in bitbyte.participants.all()]

    bitbyte_link = request.build_absolute_uri(
        reverse("candidate:bitbyte"))
    html_content = render_to_string(
        'candidate/bitbyte_confirm_email.html',
        {
            'subject': subject,
            'confirmed': confirmed,
            'participants': bitbyte.participants.all(),
            'bitbyte_link': bitbyte_link,
            'img_link': get_rand_photo(),
        }
    )
    msg = EmailMultiAlternatives(subject, subject,
                settings.NO_REPLY_EMAIL, participant_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


""" What the event types are called on admin site.
    Code will not work if they're called something else!! """
map_event_vars = {
    settings.MANDATORY_EVENT: 'Mandatory',
    settings.FUN_EVENT: 'Fun',
    settings.BIG_FUN_EVENT: 'Big Fun',
    settings.SERV_EVENT: 'Serv',
    settings.PRODEV_EVENT: 'Prodev',
    settings.HANGOUT_EVENT: 'Hangout',
    settings.BITBYTE_ACTIVITY: "Bit-Byte",
}

# TODO: support more flexible typing and string-to-var parsing/conversion
def sort_rsvps_into_events(rsvps):
    """ Takes in all confirmed rsvps and sorts them into types, currently hard coded. """
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    sorted_events = dict.fromkeys(map_event_vars.keys())
    for event_key, event_type in map_event_vars.items():
        temp = []
        for rsvp in rsvps.filter(event__event_type__type=event_type):
            temp.append(rsvp.event)
        sorted_events[event_key] = temp
    return sorted_events


def get_unconfirmed_events(rsvps, date):
    unconfirmed_events = sort_rsvps_into_events(rsvps.filter(confirmed=False))
    curr_sem_start, curr_sem_end = get_semester_bounds(date)

    # We want to show all mandatory events, not just the events the candidate has RSVP'd to
    # Get all mandatory events i.e. events with event type "Mandatory"
    mandatory_events = Event.objects.filter(
        event_type__type=map_event_vars[settings.MANDATORY_EVENT],
        start_time__gt=curr_sem_start,
        end_time__lt=curr_sem_end,
    )

    # Initialize unconfirmed_events[settings.MANDATORY_EVENT]
    if settings.MANDATORY_EVENT not in unconfirmed_events:
        unconfirmed_events[settings.MANDATORY_EVENT] = []

    for mandatory_event in mandatory_events:
        # If no rsvps are found, add this mandatory event to the list of unconfirmed events
        if rsvps.filter(event__id=mandatory_event.id).count() == 0:
            unconfirmed_events[settings.MANDATORY_EVENT].append(mandatory_event)

    return unconfirmed_events


# TODO: increase flexibility by fetching event requirement count from database
req_list = {
    settings.MANDATORY_EVENT: 3,
    settings.FUN_EVENT: 3,
    settings.BIG_FUN_EVENT: 1,
    settings.SERV_EVENT: 1,
    settings.PRODEV_EVENT: 1,
    settings.HANGOUT_EVENT: {
        settings.HANGOUT_ATTRIBUTE_NAME: 1,
        settings.CHALLENGE_ATTRIBUTE_NAME: 1,
        settings.EITHER_ATTRIBUTE_NAME: 2,
    },
    settings.BITBYTE_ACTIVITY: 3,
}

def check_requirements(confirmed_events, unconfirmed_events, num_challenges, num_bitbytes):
    """ Checks which requirements have been fulfilled by a candidate. """
    req_statuses = dict.fromkeys(req_list.keys(), False)
    req_remaining = req_list.copy()

    for req_type, minimum in req_list.items():
        if req_type == settings.BITBYTE_ACTIVITY:
            num_confirmed = num_bitbytes
        else:
            num_confirmed = len(confirmed_events[req_type])
        # officer hangouts and mandatory events are special cases
        if req_type == settings.HANGOUT_EVENT:
            interactivities = {
                settings.HANGOUT_ATTRIBUTE_NAME: num_confirmed,
                settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                settings.EITHER_ATTRIBUTE_NAME: num_confirmed + num_challenges,
            }
            req_statuses[req_type], req_remaining[req_type] = check_interactivity_requirements(interactivities)
        elif req_type == settings.MANDATORY_EVENT:
            req_remaining[req_type] = len(unconfirmed_events[settings.MANDATORY_EVENT])
            req_statuses[req_type] = req_remaining[req_type] == 0
        elif num_confirmed >= minimum:
            req_statuses[req_type] = True
            req_remaining[req_type]= max(minimum - num_confirmed, 0)

    return req_statuses, req_remaining

INTERACTIVITY_REQUIREMENTS = req_list[settings.HANGOUT_EVENT]
INTERACTIVITY_NAMES = {
    settings.EITHER_ATTRIBUTE_NAME: "Interactivities",
    settings.HANGOUT_ATTRIBUTE_NAME: "Officer Hangouts",
    settings.CHALLENGE_ATTRIBUTE_NAME: "Officer Challenges",
}

def check_interactivity_requirements(interactivities):
    """ Returns whether officer interactivities are satisfied. """
    req_remaining = {}
    for req_type, num_required in INTERACTIVITY_REQUIREMENTS.items():
        req_remaining[req_type] = max(num_required - interactivities[req_type], 0)

    req_status = not any(req_remaining.values())

    return req_status, req_remaining


def create_title(req_type: str, req_remaining: int, names: dict=map_event_vars, num_required:dict=req_list) -> str:
    if req_type == settings.MANDATORY_EVENT:
        return REQUIREMENT_TITLES_MANDATORY
    elif req_type == settings.HANGOUT_EVENT:
        return {name: create_title(name, num_required[req_type], INTERACTIVITY_NAMES, num_required[req_type]) for name in INTERACTIVITY_NAMES}
    else:
        return REQUIREMENT_TITLES_TEMPLATE.format(
            name=names[req_type],
            num_required=num_required[req_type],
            num_remaining=req_remaining[req_type],
        )


def get_requirement_colors() -> dict:
    req_colors = dict.fromkeys(map_event_vars.keys(), "grey")
    for view_key, admin_key in map_event_vars.items():
        event_type = EventType.objects.filter(type=admin_key).first()
        if event_type:
            req_colors[view_key] = event_type.color
    
    return req_colors
