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

    enableGrandTotal = models.BooleanField(
        default=False,
        help_text='Toggle the "Grant Total" field, which will take over the weighted sum total (otherwise, will use weighted sum total) (only needed for the first node)',
    )
    grandTotal = models.FloatField(
        default=0.0,
        help_text="The grand total points needed from the weighted sum of connected events (only needed for the first node)",
    )

    # Default color: CS61A blue
    color = models.CharField(max_length=7, default="#0072c1")

    def __str__(self):
        eventEntriesText = " + ".join(
            str(entry) for entry in self.mergeeventsmultiplierentry_set.all()
        )

        # Display Title and if on
        titleText = ""
        if self.title:
            titleText = " - " + self.title
            if not self.enableTitle:
                titleText += " (Title not used)"
        elif self.enableTitle:
            titleText = " - (Title is blank)"

        # Display Grand Total if on
        grandTotalText = ""
        if self.enableGrandTotal:
            grandTotalText = " - Grand Total: {}".format(self.grandTotal)

        return "{}: {}{} - {}{}{}".format(
            self.id,
            self.candidateSemesterActive,
            titleText,
            eventEntriesText,
            grandTotalText,
            "" if self.enable else " [Off]",
        )


class MergeEventsMultiplierEntry(models.Model):
    requirementMergeRequirement = models.ForeignKey(
        RequirementMergeRequirement, on_delete=models.CASCADE
    )
    enable = models.BooleanField(
        default=False,
        help_text="Toggle this entry",
    )
    eventType = models.ForeignKey("events.EventType", on_delete=models.CASCADE)
    multiplier = models.FloatField(default=1)

    def __str__(self):
        multiplier = self.multiplier
        if self.multiplier.is_integer():
            multiplier = int(self.multiplier)
        entry_string = "{} x {}".format(multiplier, self.eventType)
        if not self.enable:
            entry_string = f"({entry_string} - Disabled)"
        return entry_string
