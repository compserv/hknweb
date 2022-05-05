from django.conf import settings
from django.db import models

from hknweb.candidate.models.constants import MAX_STRLEN, MAX_TXTLEN


class OffChallenge(models.Model):
    """
    Model for an officer challenge submitted by a candidate.
    Each candidate who did the challenge must submit a separate request
    (May be changed in the future).
    Assumes the existence of two groups, "candidate" and "officer" (defined in common.py).

    For officer_confirmed and csec_confirmed, I chose to use nullable booleans
    instead of enums because they display more nicely on the admin site.
    True means it's confirmed, False means rejected, and Null means it's not reviewed yet.
    """

    class Meta:
        verbose_name = "Officer challenge"

    # the requester needs permission to add officer challenges. This limits the choices in a dropdown,
    # but the view CandRequestView is still able to set requesters regardless of their permissions
    requester = models.ForeignKey(
        "auth.User",
        # NOTE: for some reason this causes an error when you try to save on the admin, so I'll just comment it out for now
        # limit_choices_to=Q(groups__permissions__codename='add_offchallenge'),
        on_delete=models.CASCADE,
        default=None,
        related_name="received_challenges",
    )
    officer = models.ForeignKey(
        "auth.User",
        limit_choices_to={"groups__name": settings.OFFICER_GROUP},
        on_delete=models.CASCADE,
        default=None,
        related_name="given_challenges",
    )
    name = models.CharField(max_length=MAX_STRLEN, default="", verbose_name="title")
    proof = models.CharField(max_length=MAX_STRLEN, blank=True, default="")
    # whether officer confirmed this request, null when unreviewed
    officer_confirmed = models.BooleanField(null=True)
    request_date = models.DateTimeField(auto_now_add=True)

    @property
    def confirmed(self):
        return self.officer_confirmed is True

    @property
    def rejected(self):
        return self.officer_confirmed is False

    def __str__(self):
        return self.name
