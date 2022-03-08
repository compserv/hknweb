from django.conf import settings


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


def check_interactivity_requirements(interactivities, interactivity_requirements):
    """Returns whether officer interactivities are satisfied."""
    req_remaining = {}
    for req_type, num_required in interactivity_requirements.items():
        req_remaining[req_type] = max(num_required - interactivities[req_type], 0)

    req_status = not any(req_remaining.values())

    return req_status, req_remaining
