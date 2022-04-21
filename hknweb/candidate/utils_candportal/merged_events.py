from typing import Iterable, Tuple

from hknweb.coursesemester.models import Semester

from hknweb.candidate.models import RequirementMergeRequirement


class MergedEvents:
    def __init__(
        self,
        merge_requirement: RequirementMergeRequirement,
        candidateSemester: Semester,
    ):
        self.multiplier_event = {}
        self.color = merge_requirement.color
        self.title = ""
        if merge_requirement.enableTitle:
            self.title = merge_requirement.title
        self.grand_total = None
        if merge_requirement.enableGrandTotal:
            self.grand_total = merge_requirement.grandTotal

        for entry in merge_requirement.MergeEventsEntry_set.all():
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

    def get_counts(self, req_remaining: dict, req_list: dict) -> Tuple[float, float]:
        remaining_count = 0.0
        grand_total = 0.0
        for event, multiplier in zip(self.events(), self.multiplier()):
            remaining_count += multiplier * req_remaining.get(event, 1)
            grand_total += multiplier * req_list.get(event, 0)
        if self.grand_total is not None:
            grand_total = self.grand_total
        if remaining_count.is_integer() and grand_total.is_integer():
            remaining_count = int(remaining_count)
            grand_total = int(grand_total)
        return remaining_count, grand_total

    def events(self) -> Iterable:
        return self.multiplier_event.keys()

    def multiplier(self) -> Iterable:
        return self.multiplier_event.values()
