from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.db.models import Q

import itertools
from typing import Union

from hknweb.utils import get_rand_photo, get_semester_bounds
from hknweb.thread import ThreadTask

from ..events.models import Event, EventType
from .models import BitByteActivity, OffChallenge, RequirementHangout, \
                    RequirementMergeRequirement

from .constants import REQUIREMENT_TITLES_TEMPLATE, REQUIREMENT_TITLES_ALL

MANDATORY = "Mandatory"


def send_challenge_confirm_email(request, challenge, confirmed):
    subject = "[HKN] Your officer challenge was reviewed"
    candidate_email = challenge.requester.email

    challenge_link = request.build_absolute_uri(
        reverse("candidate:detail", kwargs={"pk": challenge.id})
    )
    html_content = render_to_string(
        "candidate/challenge_confirm_email.html",
        {
            "subject": subject,
            "confirmed": confirmed,
            "officer_name": challenge.officer.get_full_name(),
            "officer_username": challenge.officer.username,
            "challenge_link": challenge_link,
            "img_link": get_rand_photo(),
        },
    )
    msg = EmailMultiAlternatives(
        subject, subject, settings.NO_REPLY_EMAIL, [candidate_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_bitbyte_confirm_email(request, bitbyte, confirmed):
    subject = "[HKN] Your bit-byte request was reviewed"
    participant_emails = [part.email for part in bitbyte.participants.all()]

    bitbyte_link = request.build_absolute_uri(reverse("candidate:bitbyte"))
    html_content = render_to_string(
        "candidate/bitbyte_confirm_email.html",
        {
            "subject": subject,
            "confirmed": confirmed,
            "participants": bitbyte.participants.all(),
            "bitbyte_link": bitbyte_link,
            "img_link": get_rand_photo(),
        },
    )
    msg = EmailMultiAlternatives(
        subject, subject, settings.NO_REPLY_EMAIL, participant_emails
    )
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
    """Takes in all confirmed rsvps and sorts them into types."""
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    # sorted_events = dict.fromkeys(map_event_vars.keys())
    sorted_events = {}
    for event_type in required_events:
        temp = []
        event_time_range = required_events[event_type]
        query = Q(event__event_type__type=event_type)
        if event_time_range is not None:
            if event_time_range["eventsDateStart"] is not None:
                query = query & Q(
                    event__start_time__gt=event_time_range["eventsDateStart"]
                )
            if event_time_range["eventsDateEnd"] is not None:
                query = query & Q(event__end_time__lt=event_time_range["eventsDateEnd"])
        for rsvp in rsvps.filter(query):
            temp.append(rsvp.event)
        sorted_events[event_type] = temp
    return sorted_events


def get_events(
    rsvps, date, required_events, candidateSemester, requirement_mandatory, confirmed
):
    rsvp_models = rsvps.filter(confirmed=confirmed)
    events = sort_rsvps_into_events(rsvp_models, required_events)

    # We want to show all mandatory events, not just the events the candidate has RSVP'd to
    # Get all mandatory events i.e. events with event type "Mandatory"
    if candidateSemester and requirement_mandatory:
        mandatory_events = requirement_mandatory.events.all()
        if (
            requirement_mandatory.eventsDateStart
            and requirement_mandatory.eventsDateEnd
        ):
            mandatory_events = itertools.chain(
                mandatory_events,
                Event.objects.filter(
                    event_type__type=MANDATORY,
                    start_time__gt=requirement_mandatory.eventsDateStart,
                    end_time__lt=requirement_mandatory.eventsDateEnd,
                ),
            )
    else:
        curr_sem_start, curr_sem_end = get_semester_bounds(date)
        mandatory_events = Event.objects.filter(
            event_type__type=MANDATORY,
            start_time__gt=curr_sem_start,
            end_time__lt=curr_sem_end,
        )

    # Initialize events[MANDATORY] if hasn't
    if MANDATORY not in events:
        events[MANDATORY] = []

    # Can assume Mandatory Events where user RSVPed to is SEPARATE from those that they don't RSVP to
    if not confirmed:
        # Only add the non-rsvped Mandatory events to the Not Confirmed list
        mandatorySet = {}
        for mandatory_event in mandatory_events:
            # If no rsvps are found, add this mandatory event to the list of unconfirmed events
            if rsvps.filter(event__id=mandatory_event.id).count() == 0:
                mandatorySet[mandatory_event.id] = mandatory_event
        events[MANDATORY].extend(mandatorySet.values())

    events[MANDATORY].sort(key=lambda x: x.start_time)

    return events

def count_challenges(requested_user, candidateSemester):
    challenges = OffChallenge.objects.filter(requester__exact=requested_user)
    req_challenges_models = RequirementHangout.objects.filter(
                            eventType=settings.CHALLENGE_ATTRIBUTE_NAME,
                            candidateSemesterActive=candidateSemester,
                        ).first()
    if req_challenges_models is not None:
        if req_challenges_models.hangoutsDateStart is not None:
            challenges = challenges.filter(
                request_date__gt=req_challenges_models.hangoutsDateStart,
            )
        if req_challenges_models.hangoutsDateEnd is not None:
            challenges = challenges.filter(
                request_date__lt=req_challenges_models.hangoutsDateEnd,
            )
    # if either one is waiting, challenge is still being reviewed
    
    ## Count number of confirmed
    challenges_confirmed = challenges.filter(
        Q(officer_confirmed=True) & Q(csec_confirmed=True)
    )
    num_challenges_confirmed = challenges_confirmed.count()
    ##

    ## Count number of rejected
    challenges_rejected = challenges.filter(
        Q(officer_confirmed=False) | Q(csec_confirmed=False)
    )
    num_challenges_rejected = challenges_rejected.count()
    ##

    num_pending = challenges.count() - num_challenges_confirmed - num_challenges_rejected

    return num_challenges_confirmed, num_challenges_rejected, num_pending

def count_num_bitbytes(requested_user, bitbyte_requirement):
    bitbyte_models = BitByteActivity.objects.filter(
                        participants__exact=requested_user,
                        confirmed=True
                    )
    if bitbyte_requirement is not None:
        if bitbyte_requirement.bitByteDateStart is not None:
            bitbyte_models = bitbyte_models.filter(
                request_date__gt=bitbyte_requirement.bitByteDateStart,
            )
        if bitbyte_requirement.bitByteDateEnd is not None:
            bitbyte_models = bitbyte_models.filter(
                request_date__lt=bitbyte_requirement.bitByteDateEnd,
            )
    num_bitbytes = bitbyte_models.count()
    return num_bitbytes

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


def check_requirements(
    confirmed_events, unconfirmed_events, num_challenges, num_bitbytes, req_list
):
    """Checks which requirements have been fulfilled by a candidate."""
    req_statuses = dict.fromkeys(req_list.keys(), False)
    req_remaining = {**req_list}  # Makes deep copy of "req_list"

    for req_type, minimum in req_list.items():
        num_confirmed = 0
        if req_type == settings.BITBYTE_ACTIVITY:
            num_confirmed = num_bitbytes
        elif req_type in confirmed_events:
            num_confirmed = len(confirmed_events[req_type])
        # officer hangouts and mandatory events are special cases
        if req_type == settings.HANGOUT_EVENT:
            # TODO: Hardcoded-ish for now, allow for choice of Hangout events
            if "Hangout" in confirmed_events:
                num_confirmed = len(confirmed_events["Hangout"])
            interactivities = {
                settings.HANGOUT_ATTRIBUTE_NAME: num_confirmed,
                settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                settings.EITHER_ATTRIBUTE_NAME: num_confirmed + num_challenges,
            }
            (
                req_statuses[req_type],
                req_remaining[req_type],
            ) = check_interactivity_requirements(
                interactivities, req_list[settings.HANGOUT_EVENT]
            )
        elif (minimum < 0) or (minimum is None):  # settings.MANDATORY_EVENT:
            req_remaining[req_type] = len(
                unconfirmed_events[req_type]
            )  # len(unconfirmed_events[settings.MANDATORY_EVENT])
            req_statuses[req_type] = req_remaining[req_type] == 0
        else:
            req_statuses[req_type] = num_confirmed >= minimum
            req_remaining[req_type] = max(minimum - num_confirmed, 0)

    return req_statuses, req_remaining


# INTERACTIVITY_REQUIREMENTS = req_list[settings.HANGOUT_EVENT]
INTERACTIVITY_NAMES = {
    settings.EITHER_ATTRIBUTE_NAME: "Interactivities",
    settings.HANGOUT_ATTRIBUTE_NAME: "Officer Hangouts",
    settings.CHALLENGE_ATTRIBUTE_NAME: "Officer Challenges",
}


def check_interactivity_requirements(interactivities, interactivity_requirements):
    """Returns whether officer interactivities are satisfied."""
    req_remaining = {}
    for req_type, num_required in interactivity_requirements.items():
        req_remaining[req_type] = max(num_required - interactivities[req_type], 0)

    req_status = not any(req_remaining.values())

    return req_status, req_remaining


def create_title(
    req_type: str,
    req_remaining: Union[dict, int],
    name: str,
    num_required: int,
    num_required_hangouts: dict,
) -> str:
    if type(num_required) == int and (
        num_required < 0 or (num_required is None)
    ):  # settings.MANDATORY_EVENT:
        return REQUIREMENT_TITLES_ALL.format(name=name)
    elif req_type == settings.HANGOUT_EVENT:
        return {
            name: create_title(
                name,
                req_remaining[name],
                INTERACTIVITY_NAMES[name],
                num_required_hangouts[name],
                None,
            )
            for name in num_required_hangouts
        }
    else:
        return REQUIREMENT_TITLES_TEMPLATE.format(
            name=name,
            num_required=num_required,
            num_remaining=req_remaining,
        )


def get_requirement_colors(
    required_events,
    color_source=lambda view_key: EventType.objects.get(type=view_key),
    get_key=lambda x: x,
) -> dict:
    req_colors = {}
    for event in required_events:
        view_key = get_key(event)
        event_type = color_source(event)
        if event_type:
            req_colors[view_key] = event_type.color
        else:
            req_colors[view_key] = "grey"

    return req_colors


class MergedEvents:
    def __init__(
        self,
        merger_node: RequirementMergeRequirement,
        candidateSemester,
        seen_merger_nodes=set(),
    ):
        assert merger_node.enable, "The first Merger Node must be enabled"

        seen_merger_nodes.clear()
        current_merger_node = merger_node

        self.multiplier_event = {}
        self.all_required = False
        self.color = merger_node.color
        self.title = ""
        if merger_node.enableTitle:
            self.title = merger_node.title
        self.grand_total = None
        if merger_node.enableGrandTotal:
            self.grand_total = merger_node.grandTotal

        while current_merger_node is not None:
            if current_merger_node.id in seen_merger_nodes:
                self.all_required = True
                break
            seen_merger_nodes.add(current_merger_node.id)
            eventTypeKey = current_merger_node.event1.type
            self.multiplier_event[eventTypeKey] = (
                self.multiplier_event.get(eventTypeKey, 0)
                + current_merger_node.multiplier1
            )
            if current_merger_node.event2 is not None:
                eventTypeKey2 = current_merger_node.event2.type
                self.multiplier_event[eventTypeKey2] = (
                    self.multiplier_event.get(eventTypeKey2, 0)
                    + current_merger_node.multiplier2
                )
            if current_merger_node.linkedRequirement:
                current_merger_node = RequirementMergeRequirement.objects.filter(
                    candidateSemesterActive=candidateSemester.id,
                    id=current_merger_node.linkedRequirement.id,
                ).first()
            else:
                current_merger_node = None

    def __str__(self):
        text = self.get_events_str()
        all_required_text = "self.all_required = {}".format(self.all_required)
        all_color_text = "self.color = {}".format(self.color)
        return "{}, {}, {}".format(text, all_required_text, all_color_text)

    def get_events_str(self):
        if self.title:
            return self.title
        text = []
        for event, multiplier in zip(self.events(), self.multiplier()):
            if multiplier != 1.0:
                text.append(str(multiplier) + " x " + event)
            else:
                text.append(event)
        self.title = " + ".join(text)
        return self.title

    def get_counts(self, req_remaining, req_list):
        remaining_count = 0
        grand_total = 0
        for event, multiplier in zip(self.events(), self.multiplier()):
            remaining_count += multiplier * req_remaining.get(event, 0)
            grand_total += multiplier * req_list.get(event, 0)
        if self.grand_total is not None:
            grand_total = self.grand_total
        return remaining_count, grand_total

    def events(self):
        return self.multiplier_event.keys()

    def multiplier(self):
        return self.multiplier_event.values()

NO_ACTION_PLS_FIX = "No candidate account actions have been taken, so re-upload the entire file after fixing the errors."

def spawn_threaded_add_cands_and_email(cand_csv):
    task = ThreadTask()
    task.save()
    t = threading.Thread(target=threaded_add_cands_and_email,args=[cand_csv, task])
    t.setDaemon(True)
    t.start()
    return task.id

def threaded_add_cands_and_email(cand_csv, task):
    try:
        result, msg = add_cands_and_email(cand_csv, task)
    except Exception as e:
        result = False
        msg = str(e)
    task.message = msg
    if result:
        task.complete()
    else:
        task.failure()
    task.progress = 100
    task.save()

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

def add_cands_and_email(cand_csv, task=None):
    candidate_group = Group.objects.get(name=ATTR.CANDIDATE)
    progress_float = 0.0
    CAND_ACC_WEIGHT = 0.25
    EMAIL_WEIGHT = 0.75

    # Sanity check progress
    if task is not None:
        task.progress = 1

    # Pre-screen and validate data
    new_cand_list = []
    email_set = set()
    username_set = set()
    current_cand_semester = get_current_cand_semester()
    email_passwords = {}
    if current_cand_semester is None:
        error_msg = "Inform CompServ the following: Please add the current semester in CourseSemester."
        error_msg += " "
        error_msg += NO_ACTION_PLS_FIX
        return False, error_msg
    for i, row in enumerate(cand_csv):
        # if i >= 30:
        #     error_msg = "Preprocessing stopped! Detected more than 30 account requests!"
        #     error_msg += " "
        #     error_msg += "Please upload the file in separate batches of 30 account requests each."
        #     error_msg += " "
        #     error_msg += NO_ACTION_PLS_FIX
        #     return False, error_msg
        try:
            candidatedto = CandidateDTO(row)
        except AssertionError as e:
            error_msg = "Invalid CSV format. Check that your columns are correctly labeled, there are NO blank rows, and filled out for each row."
            error_msg += " "
            error_msg += NO_ACTION_PLS_FIX
            error_msg += " "
            error_msg += "Candidate error message: {}.".format(e)
            error_msg += " "
            error_msg += "Row Information at row {}: {}.".format(i + 1, row)
            return False, error_msg

        password = BaseUserManager.make_random_password(
            None, length=DEFAULT_RANDOM_PASSWORD_LENGTH
        )
        
        duplicate, error_msg = check_duplicates(candidatedto, row, email_set, username_set, i)
        if duplicate:
            return False, error_msg
        
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

    # Since no number of rows avaiable, can't live track progress
    progress_float = CAND_ACC_WEIGHT * 100
    if task is not None:
        task.progress = round(progress_float)
    
    num_of_accounts = len(email_set)
    
    # Release the memory once done
    del email_set
    del username_set
    
    # Add all candidates
    count = 0
    
    email_errors = []
    for i, new_cand in enumerate(new_cand_list):
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
        try:
            msg.send()
        except Exception as e:
            email_errors.append((new_cand_list[i].email, str(e)))
        
        progress_float += EMAIL_WEIGHT * 100 * (i + 1)/num_of_accounts
        if task is not None:
            task.progress = round(progress_float)
        
    
    # If gone through everything and no errors
    if len(email_errors) > 0:
        error_msg = "An error occured during the sending of emails. " \
                    + "Candidate Email and Error Messages: " + str(email_errors) + " --- " \
                    + "Inform CompServ of the errors, and inform the candidates " \
                    + "to access their accounts by resetting their password " \
                    + "using \"Forget your password?\" in the Login page. " \
                    + "All {} candidates added!".format(count)
        return False, error_msg
    else:
        return True, "Successfully added {} candidates!".format(count)

