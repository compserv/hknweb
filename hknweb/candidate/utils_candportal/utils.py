from typing import Callable, Union

from django.conf import settings

from hknweb.events.models import EventType

from hknweb.candidate.constants import REQUIREMENT_TITLES_TEMPLATE, EVENT_NAMES


INTERACTIVITY_NAMES = {
    EVENT_NAMES.EITHER: "Interactivities",
    EVENT_NAMES.HANGOUT: "Officer Hangouts",
    EVENT_NAMES.CHALLENGE: "Officer Challenges",
}


def create_title(
    req_type: str,
    req_remaining: Union[dict, int],
    name: str,
    num_required: int,
    num_required_hangouts: dict,
) -> str:
    if req_type == EVENT_NAMES.INTERACTIVITIES:
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
    required_events: dict,
    color_source: Callable=lambda view_key: EventType.objects.get(type=view_key),
    get_key: Callable=lambda x: x,
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
