from django.db import models
from django.utils import timezone
from django.conf import settings

MAX_STRLEN = 150 # default max length for char fields
MAX_TXTLEN = 2000 # default max length for text fields


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
    requester         = models.ForeignKey('auth.User',
    # NOTE: for some reason this causes an error when you try to save on the admin, so I'll just comment it out for now
                            # limit_choices_to=Q(groups__permissions__codename='add_offchallenge'),
                            on_delete=models.CASCADE, default=None, related_name='received_challenges')
    officer           = models.ForeignKey('auth.User', limit_choices_to={'groups__name': settings.OFFICER_GROUP},
                            on_delete=models.CASCADE, default=None, related_name='given_challenges')
    name              = models.CharField(max_length=MAX_STRLEN, default='', verbose_name="title")
    description       = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # proof of completion is optional (if proof is a file, the candiate can send it to slack)
    proof             = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # optional comment about, say, why the confirmation request was declined
    officer_comment   = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # whether officer confirmed this request, null when unreviewed
    officer_confirmed = models.BooleanField(null=True)
    # whether corresponding secretary or other admin has confirmed this request, null when unreviewed
    csec_confirmed    = models.BooleanField(null=True)
    request_date      = models.DateTimeField(auto_now_add=True)

    @property
    def confirmed(self):
        return self.officer_confirmed is True and self.csec_confirmed is True

    @property
    def rejected(self):
        return self.officer_confirmed is False or self.csec_confirmed is False

    def __str__(self):
        return self.name


class BitByteActivity(models.Model):
    """
    Model for one bit byte activity for a group of candidates.
    For each bit byte activity, one candidate must submit a request for the entire
    group on the portal, and this needs to be confirmed by VP on the admin site.
    """
    class Meta:
        verbose_name_plural = "Bit Byte Activities"

    participants = models.ManyToManyField('auth.User')
    # whether VP/Csec confirmed this request, null when unreviewed
    confirmed = models.BooleanField(null=True)
    proof = models.TextField(max_length=MAX_TXTLEN, blank=False, default='') # notes and link by candidate
    notes = models.TextField(max_length=MAX_TXTLEN, blank=True, default='') # notes by VP
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ", ".join([c.username for c in self.participants.all()]) + "; " + self.proof

    @property
    def is_confirmed(self):
        return self.confirmed is True

    @property
    def is_rejected(self):
        return self.confirmed is False



# CS 61A LECTURE NUMBER 3141592653589793238462643383
class Announcement(models.Model):
    """
    Model for an announcement. Created by VP or some other superuser.
    Displayed on the home page. The title will be displayed in bold,
    and the text will follow that in normal font, with a space in between.
    """

    title           = models.CharField(max_length=MAX_STRLEN, default='')
    text            = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # if visible == False, then admins can see announcement but it's not displayed on portal
    visible         = models.BooleanField(default=False)
    release_date    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title if self.title != '' else self.text


class CandidateForm(models.Model):

    name           = models.CharField(max_length=MAX_STRLEN, default='')
    duedate        = models.DateTimeField(default=timezone.now)
    link           = models.CharField(max_length=MAX_STRLEN, default='')
    # if visible == False, then admins can see candiate form but it's not displayed on portal
    visible         = models.BooleanField(default=False)

    def __str__(self):
        return self.name
