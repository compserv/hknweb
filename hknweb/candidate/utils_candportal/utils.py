from typing import Callable

from hknweb.events.models import EventType


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


def apply_to_dicts(fn: Callable, *ds: list) -> dict:
    for k, v in ds[0].items():
        if isinstance(v, dict):
            apply_to_dicts(fn, *[d[k] for d in ds])
        else:
            fn(k, v, *ds)
    return ds[0]
