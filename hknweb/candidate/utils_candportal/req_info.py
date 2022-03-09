from django.conf import settings

from hknweb.candidate.utils_candportal.utils import (
    create_title,
    get_requirement_colors,
)


class ReqInfo:
    def __init__(self,
        lst: dict,
        statuses: dict,
        remaining: dict,
        confirmed_events: dict,
        unconfirmed_events: dict,
    ):
        self.lst = lst
        self.statuses = statuses
        self.remaining = remaining
        self.confirmed_events = confirmed_events
        self.unconfirmed_events = unconfirmed_events

        self.titles = None
        self.colors = None

    def set_titles(self, required_events: dict):
        titles = {}
        for req_type in self.statuses:
            name = required_events.get(req_type, {}).get("title", req_type)
            if not name:
                name = req_type

            titles[req_type] = create_title(
                req_type,
                self.remaining[req_type],
                name,
                self.lst[req_type],
                self.lst.get(settings.HANGOUT_EVENT, {}),
            )

        self.titles = titles

    def set_colors(self, event_types: list, merger_nodes):
        colors = get_requirement_colors(event_types)
        colors.update(
            get_requirement_colors(
                merger_nodes,
                lambda view_key: view_key,
                lambda get_key: get_key.get_events_str(),
            )
        )

        self.colors = colors
