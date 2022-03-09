from typing import Callable, Union

from django.conf import settings

from hknweb.events.models import EventType

from hknweb.candidate.constants import (
    REQUIREMENT_TITLES_ALL,
    REQUIREMENT_TITLES_TEMPLATE,
)


INTERACTIVITY_NAMES = {
    settings.EITHER_ATTRIBUTE_NAME: "Interactivities",
    settings.HANGOUT_ATTRIBUTE_NAME: "Officer Hangouts",
    settings.CHALLENGE_ATTRIBUTE_NAME: "Officer Challenges",
}


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
