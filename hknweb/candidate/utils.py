from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import render_to_string

import itertools
from typing import Union

from hknweb.utils import get_rand_photo, get_semester_bounds

from ..events.models import EventType
from .models import RequirementMergeRequirement

from .constants import REQUIREMENT_TITLES_TEMPLATE, REQUIREMENT_TITLES_ALL

MANDATORY = "Mandatory"

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
# map_event_vars = {
#     settings.MANDATORY_EVENT: 'Mandatory',
#     settings.FUN_EVENT: 'Fun',
#     settings.BIG_FUN_EVENT: 'Big Fun',
#     settings.SERV_EVENT: 'Serv',
#     settings.PRODEV_EVENT: 'Prodev',
#     settings.HANGOUT_EVENT: 'Hangout',
#     settings.BITBYTE_ACTIVITY: "Bit-Byte",
# }

# Done: support more flexible typing and string-to-var parsing/conversion
def sort_rsvps_into_events(rsvps, required_events):
    """ Takes in all confirmed rsvps and sorts them into types, currently hard coded. """
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    # sorted_events = dict.fromkeys(map_event_vars.keys())
    sorted_events = {}
    for event_type in required_events:
        temp = []
        for rsvp in rsvps.filter(event__event_type__type=event_type):
            temp.append(rsvp.event)
        sorted_events[event_type] = temp
    return sorted_events

def get_events(rsvps, date, required_events, candidateSemester, requirement_mandatory, confirmed):
    event_models = rsvps.filter(confirmed=confirmed)
    events = sort_rsvps_into_events(event_models, required_events)
    curr_sem_start, curr_sem_end = get_semester_bounds(date)

    # We want to show all mandatory events, not just the events the candidate has RSVP'd to
    # Get all mandatory events i.e. events with event type "Mandatory"
    if candidateSemester and requirement_mandatory:
        mandatory_events = requirement_mandatory.events.all()
        if requirement_mandatory.eventsDateStart and requirement_mandatory.eventsDateEnd:
            mandatory_events = itertools.chain(mandatory_events, \
                event_models.filter(
                    event_type__type=MANDATORY,
                    start_time__gt=requirement_mandatory.eventsDateStart,
                    end_time__lt=requirement_mandatory.eventsDateEnd,
                )
            )
    else:
        mandatory_events = event_models.filter(
            event_type__type=MANDATORY,
            start_time__gt=curr_sem_start,
            end_time__lt=curr_sem_end,
        )

    # Initialize events[settings.MANDATORY_EVENT]
    if MANDATORY not in events:
        events[MANDATORY] = []

    mandatorySet = {}
    for mandatory_event in mandatory_events:
        # If no rsvps are found, add this mandatory event to the list of (un)confirmed events
        if rsvps.filter(event__id=mandatory_event.id).count() == 0:
            mandatorySet[mandatory_event.id] = mandatory_event

    events[MANDATORY].extend(mandatorySet.values())
    events[MANDATORY].sort(key=lambda x: x.start_time)

    return events

# Done: increase flexibility by fetching event requirement count from database
# req_list = {
#     settings.MANDATORY_EVENT: 3,
#     settings.FUN_EVENT: 3,
#     settings.BIG_FUN_EVENT: 1,
#     settings.SERV_EVENT: 1,
#     settings.PRODEV_EVENT: 1,
#     settings.HANGOUT_EVENT: {
#         settings.HANGOUT_ATTRIBUTE_NAME: 2,
#         settings.CHALLENGE_ATTRIBUTE_NAME: 1,
#         settings.EITHER_ATTRIBUTE_NAME: 3,
#     },
#     settings.BITBYTE_ACTIVITY: 3,
# }

def check_requirements(confirmed_events, unconfirmed_events, num_challenges, \
                        num_bitbytes, required_events, req_list):
    """ Checks which requirements have been fulfilled by a candidate. """
    req_statuses = dict.fromkeys(req_list.keys(), False)
    req_remaining = {**req_list} # Makes deep copy of "req_list"

    for req_type, minimum in req_list.items():
        num_confirmed = 0
        if req_type == settings.BITBYTE_ACTIVITY:
            num_confirmed = num_bitbytes
        elif req_type in confirmed_events:
            num_confirmed = len(confirmed_events[req_type])
        # officer hangouts and mandatory events are special cases
        if req_type == settings.HANGOUT_EVENT:
            interactivities = {
                settings.HANGOUT_ATTRIBUTE_NAME: num_confirmed,
                settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                settings.EITHER_ATTRIBUTE_NAME: num_confirmed + num_challenges,
            }
            req_statuses[req_type], req_remaining[req_type] = check_interactivity_requirements(interactivities, req_list[settings.HANGOUT_EVENT])
        elif ((minimum < 0) or (minimum is None)): #settings.MANDATORY_EVENT:
            req_remaining[req_type] = len(unconfirmed_events[req_type]) #len(unconfirmed_events[settings.MANDATORY_EVENT])
            req_statuses[req_type] = req_remaining[req_type] == 0
        else:
            req_statuses[req_type] = num_confirmed >= minimum
            req_remaining[req_type]= max(minimum - num_confirmed, 0)

    return req_statuses, req_remaining

# INTERACTIVITY_REQUIREMENTS = req_list[settings.HANGOUT_EVENT]
INTERACTIVITY_NAMES = {
    settings.EITHER_ATTRIBUTE_NAME: "Interactivities",
    settings.HANGOUT_ATTRIBUTE_NAME: "Officer Hangouts",
    settings.CHALLENGE_ATTRIBUTE_NAME: "Officer Challenges",
}

def check_interactivity_requirements(interactivities, interactivity_requirements):
    """ Returns whether officer interactivities are satisfied. """
    req_remaining = {}
    for req_type, num_required in interactivity_requirements.items():
        req_remaining[req_type] = max(num_required - interactivities[req_type], 0)

    req_status = not any(req_remaining.values())

    return req_status, req_remaining


def create_title(req_type: str, req_remaining: Union[dict, int], name: str, num_required: int, num_required_hangouts: dict) -> str:
    if type(num_required) == int and (num_required < 0 or (num_required is None)): #settings.MANDATORY_EVENT:
        return REQUIREMENT_TITLES_ALL.format(name=name)
    elif req_type == settings.HANGOUT_EVENT:
        return {name: create_title(name, req_remaining[name], INTERACTIVITY_NAMES[name], num_required_hangouts[name], None) for name in num_required_hangouts}
    else:
        return REQUIREMENT_TITLES_TEMPLATE.format(
            name=name,
            num_required=num_required,
            num_remaining=req_remaining,
        )


def get_requirement_colors(required_events, \
    color_source=lambda view_key:EventType.objects.get(type=view_key),
    get_key=lambda x:x) -> dict:
    req_colors = {}
    for event in required_events:
        view_key = get_key(event)
        event_type = color_source(event)
        if event_type:
            req_colors[view_key] = event_type.color
        else:
            req_colors[view_key] = "grey"
    
    return req_colors

class MergedEvents():
    def __init__(self, merger_node: RequirementMergeRequirement, candidateSemester, seen_merger_nodes=set()):
        assert merger_node.enable, "The first Merger Node must be enabled"
        
        seen_merger_nodes.clear()
        current_merger_node = merger_node
        
        self.multiplier_event = {}
        self.all_required = False
        self.color = merger_node.color

        while (current_merger_node is not None):
            if (current_merger_node.id in seen_merger_nodes):
                self.all_required = True
                break
            seen_merger_nodes.add(current_merger_node.id)
            eventTypeKey = current_merger_node.event1.type
            self.multiplier_event[eventTypeKey] = self.multiplier_event.get(eventTypeKey, 0) + current_merger_node.multiplier1
            if current_merger_node.event2 is not None:
                eventTypeKey2 = current_merger_node.event2.type
                self.multiplier_event[eventTypeKey2] = self.multiplier_event.get(eventTypeKey2, 0) + current_merger_node.multiplier2
            if current_merger_node.linkedRequirement:
                current_merger_node = RequirementMergeRequirement.objects.filter(candidateSemesterActive=candidateSemester.id, id=current_merger_node.linkedRequirement.id).first()
            else:
                current_merger_node = None
    
    def __str__(self):
        text = self.get_events_str()
        all_required_text = "self.all_required = {}".format(self.all_required)
        all_color_text = "self.color = {}".format(self.color)
        return "{}, {}, {}".format(text, all_required_text, all_color_text)
    
    def get_events_str(self):
        text = []
        for event, multiplier in zip(self.events(), self.multiplier()):
            if multiplier != 1.0:
                text.append(str(multiplier) + " x " + event)
            else:
                text.append(event)
        return " + ".join(text)
    
    def get_counts(self, req_remaining, req_list):
        remaining_count = 0
        grand_total = 0
        for event, multiplier in zip(self.events(), self.multiplier()):
            remaining_count += multiplier * req_remaining.get(event, 0)
            grand_total += multiplier * req_list.get(event, 0)
        return remaining_count, grand_total
    
    def events(self):
        return self.multiplier_event.keys()
    
    def multiplier(self):
        return self.multiplier_event.values()
