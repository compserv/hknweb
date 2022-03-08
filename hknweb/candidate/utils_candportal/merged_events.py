from hknweb.candidate.models import RequirementMergeRequirement


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
