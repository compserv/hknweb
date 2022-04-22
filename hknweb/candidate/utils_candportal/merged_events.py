from typing import Iterable, Tuple

from hknweb.coursesemester.models import Semester

from hknweb.candidate.models import RequirementMergeRequirement

from hknweb.candidate.utils_candportal.req_info import ReqInfo


class MergedEvents:
    def __init__(
        self,
        merge_requirement: RequirementMergeRequirement,
        candidateSemester: Semester,
    ):
        self.multiplier_event = {}
        self.color = merge_requirement.color
        self.title = ""
        self.missing_event_reqs = []
        if merge_requirement.enableTitle:
            self.title = merge_requirement.title
        self.grand_total = None
        if merge_requirement.enableGrandTotal:
            self.grand_total = merge_requirement.grandTotal

        for entry in merge_requirement.mergeeventsmultiplierentry_set.filter(enable=True):
            eventTypeKey = entry.eventType.type
            self.multiplier_event[eventTypeKey] = (
                self.multiplier_event.get(eventTypeKey, 0)
                + entry.multiplier
            )

    def __str__(self) -> str:
        text = self.get_events_str()
        all_color_text = "self.color = {}".format(self.color)
        return "{}, {}".format(text, all_color_text)

    def get_events_str(self) -> str:
        if self.title:
            return self.title
        text = []
        for event, multiplier in zip(self.events(), self.multiplier()):
            if multiplier != 1.0:
                if multiplier.is_integer():
                    multiplier = int(multiplier)
                text.append(str(multiplier) + " x " + event)
            else:
                text.append(event)
        self.title = " + ".join(text)
        return self.title

    def get_counts(self, req_info: ReqInfo) -> Tuple[float, float]:
        remaining_count = None
        credit_count = 0.0
        grand_total = 0.0
        req_list = req_info.lst
        req_remaining = req_info.remaining
        for event, multiplier in zip(self.events(), self.multiplier()):
            if (event not in req_remaining) or (event not in req_list):
                self.missing_event_reqs.append(event)
            else:
                credit_count += multiplier * req_info.confirmed[event]
                grand_total += multiplier * req_list[event]
        if self.grand_total is not None:
            grand_total = self.grand_total
            if self.check_all_missing():
                remaining_count = grand_total
        if remaining_count is None:
            remaining_count = max(grand_total - credit_count, 0)
        if remaining_count.is_integer() and grand_total.is_integer():
            remaining_count = int(remaining_count)
            grand_total = int(grand_total)
        missing_event_reqs_text = None
        if self.missing_event_reqs:
            missing_event_reqs_text = "Missing RequiredEvents: {}".format(self.missing_event_reqs)
        return remaining_count, grand_total, missing_event_reqs_text
    
    def check_all_missing(self) -> bool:
        return len(self.missing_event_reqs) == len(self.multiplier_event)

    def events(self) -> Iterable:
        return self.multiplier_event.keys()

    def multiplier(self) -> Iterable:
        return self.multiplier_event.values()
