from django.db import models

from hknweb.candidate.models.constants import MAX_STRLEN


class BitByteActivity(models.Model):
    """
    Model for one bit byte activity for a group of candidates.
    For each bit byte activity, one candidate must submit a request for the entire
    group on the portal, and this needs to be confirmed by VP on the admin site.
    """

    class Meta:
        verbose_name_plural = "Bit Byte Activities"

    participants = models.ManyToManyField("auth.User")
    # whether VP/Csec confirmed this request, null when unreviewed
    confirmed = models.BooleanField(null=True)
    proof = models.CharField(
        max_length=MAX_STRLEN, blank=False, default=""
    )  # notes and link by candidate
    notes = models.CharField(
        max_length=MAX_STRLEN, blank=True, default=""
    )  # notes by VP
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            ", ".join([c.username for c in self.participants.all()]) + "; " + self.proof
        )

    @property
    def is_confirmed(self):
        return self.confirmed is True

    @property
    def is_rejected(self):
        return self.confirmed is False
