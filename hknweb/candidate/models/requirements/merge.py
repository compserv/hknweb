from django.db import models
from hknweb.coursesemester.models import Semester

from hknweb.candidate.models.constants import MAX_STRLEN


class RequirementMergeRequirement(models.Model):
    enableTitle = models.BooleanField(default=False)
    title = models.CharField(max_length=MAX_STRLEN, default="", blank=True)

    enable = models.BooleanField(
        default=False,
        help_text="Toggle this Merge node (when ON, this will exist as a first node) (Ignored if it is a connected node)",
    )
    candidateSemesterActive = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Candidate semester this Merged Requirement will take place (ignored if it is a connected node)",
    )

    event1 = models.ForeignKey(
        "events.EventType", on_delete=models.SET_NULL, null=True, related_name="event1"
    )
    multiplier1 = models.FloatField(default=1)

    event2 = models.ForeignKey(
        "events.EventType",
        on_delete=models.SET_NULL,
        null=True,
        related_name="event2",
        blank=True,
    )
    multiplier2 = models.FloatField(default=1)

    enableGrandTotal = models.BooleanField(
        default=False,
        help_text='Toggle the "Grant Total" field, which will take over the weighted sum total (otherwise, will use weighted sum total) (only needed for the first node)',
    )
    grandTotal = models.FloatField(
        default=None,
        null=True,
        help_text="The grand total points needed from the weighted sum of connected events (only needed for the first node)",
    )

    # Default color: CS61A blue
    color = models.CharField(max_length=7, default="#0072c1")

    linkedRequirement = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Connect to another Merged Requirement node here (Candidate Semester, Grand Total, and all Enable fields for all subsequent connected nodes will be ignored) (A Cycle will make the Grand Total equal Infinite (higher precidence to Grand Total and weighted total sum))",
    )

    def __str__(self):
        event2Text = ""
        if self.event2 is not None:
            event2Text = " + {} x {}".format(self.multiplier2, self.event2)
        linkedRequirementText = ""
        if self.linkedRequirement is not None:
            linkedRequirementText = " - Linked with: {}".format(
                self.linkedRequirement.id
            )
        titleText = ""
        if self.title:
            titleText = " - " + self.title
            if not self.enableTitle:
                titleText += " (Title not used)"
        elif self.enableTitle:
            titleText = " - (Title is blank)"
        return "{}: {}{} - {} x {}{}{}{}".format(
            self.id,
            self.candidateSemesterActive,
            titleText,
            self.multiplier1,
            self.event1,
            event2Text,
            linkedRequirementText,
            "" if self.enable else " [Off]",
        )
