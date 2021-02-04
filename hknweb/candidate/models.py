from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from hknweb.coursesemester.models import Semester

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
    visible        = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.candidateSemesterActive)

class CandidateFormDoneEntry(models.Model):
    users      = models.ManyToManyField(User)
    form       = models.OneToOneField(CandidateForm, models.CASCADE)
    notes      = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Candidate Form Done Entries"
    
    def __str__(self):
        return "Forms filled for: {}".format(self.form)

class DuePayment(models.Model):
    name           = models.CharField(max_length=MAX_STRLEN, default='')
    duedate        = models.DateTimeField(default=timezone.now)
    instructions   = models.CharField(max_length=MAX_STRLEN, default='', blank=True)
    # if visible == False, then admins can see candiate form but it's not displayed on portal
    visible        = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.candidateSemesterActive)

class DuePaymentPaidEntry(models.Model):
    users           = models.ManyToManyField(User)
    duePayment      = models.OneToOneField(DuePayment, models.CASCADE)
    notes           = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Due Payment Paid Entries"
    
    def __str__(self):
        return "Payments for: {}".format(self.duePayment)

class CommitteeProject(models.Model):
    name           = models.CharField(max_length=MAX_STRLEN, default='')
    duedate        = models.DateTimeField(default=timezone.now)
    instructions   = models.CharField(max_length=MAX_STRLEN, default='', blank=True)
    # if visible == False, then admins can see candiate form but it's not displayed on portal
    visible        = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.candidateSemesterActive)

class CommitteeProjectDoneEntry(models.Model):
    users                  = models.ManyToManyField(User)
    committeeProject       = models.OneToOneField(CommitteeProject, models.CASCADE)
    notes                  = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Committee Project Done Entries"
    
    def __str__(self):
        return "Committee Project completed for: {}".format(self.committeeProject)

class RequriementEvent(models.Model):
    enableTitle = models.BooleanField(default=False)
    title = models.CharField(max_length=MAX_STRLEN, default='', blank=True)
    
    eventType = models.ForeignKey('events.EventType', on_delete=models.CASCADE)
    numberRequired = models.IntegerField(default=0)
    enable = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    eventsDateStart = models.DateTimeField(null=True, blank=True)
    eventsDateEnd = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        numReqText = self.numberRequired
        if self.numberRequired < 0 or (self.numberRequired is None):
            numReqText = "All"
        return "{} {} Event - Number Required: {}{}".format(self.candidateSemesterActive, \
            self.eventType, numReqText, "" if self.enable else " [Off]")

class RequirementHangout(models.Model):
    eventType = models.CharField(max_length=255, choices=[ \
        (settings.HANGOUT_ATTRIBUTE_NAME, "Officer Hangouts"),
        (settings.CHALLENGE_ATTRIBUTE_NAME, "Officer Challenges"),
        (settings.EITHER_ATTRIBUTE_NAME, "Either")
    ])
    numberRequired = models.IntegerField(default=0)
    enable = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    hangoutsDateStart = models.DateTimeField(null=True, blank=True)
    hangoutsDateEnd = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "{} {} - Number Required: {}{}".format(self.candidateSemesterActive, self.eventType, self.numberRequired, "" if self.enable else " [Off]")

class RequirementMandatory(models.Model):
    enable = models.BooleanField(default=False)
    events = models.ManyToManyField('events.Event')
    candidateSemesterActive = models.OneToOneField(Semester, on_delete=models.SET_NULL, null=True)
    eventsDateStart = models.DateTimeField(null=True, blank=True)
    eventsDateEnd = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} Mandatory - {} to {}{}".format(self.candidateSemesterActive, self.eventsDateStart, self.eventsDateEnd, "" if self.enable else " [Off]")

class RequirementBitByteActivity(models.Model):
    enable = models.BooleanField(default=False)
    candidateSemesterActive = models.OneToOneField(Semester, on_delete=models.SET_NULL, null=True)
    numberRequired = models.IntegerField(default=0)

    def __str__(self):
        return "{} - Number Required: {}{}".format(self.candidateSemesterActive, self.numberRequired, "" if self.enable else " [Off]")

class RequirementMergeRequirement(models.Model):
    enableTitle = models.BooleanField(default=False)
    title = models.CharField(max_length=MAX_STRLEN, default='', blank=True)

    enable = models.BooleanField(default=False, help_text="Toggle this Merge node (when ON, this will exist as a first node) (Ignored if it is a connected node)")
    candidateSemesterActive = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, help_text="Candidate semester this Merged Requirement will take place (ignored if it is a connected node)")

    event1 = models.ForeignKey('events.EventType', on_delete=models.SET_NULL, null=True, related_name='event1')
    multiplier1 = models.FloatField(default=1)
    
    event2 = models.ForeignKey('events.EventType', on_delete=models.SET_NULL, null=True, related_name='event2', blank=True)
    multiplier2 = models.FloatField(default=1)

    enableGrandTotal = models.BooleanField(default=False, help_text="Toggle the \"Grant Total\" field, which will take over the weighted sum total (otherwise, will use weighted sum total) (only needed for the first node)")
    grandTotal = models.FloatField(default=None, null=True, help_text="The grand total points needed from the weighted sum of connected events (only needed for the first node)")

    # Default color: CS61A blue
    color = models.CharField(max_length=7, default="#0072c1")

    linkedRequirement = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                          help_text="Connect to another Merged Requirement node here (Candidate Semester, Grand Total, and all Enable fields for all connected nodes will be ignored) (A Cycle will make the Grand Total equal Infinite (higher precidence to Grand Total and weighted total sum))")

    def __str__(self):
        event2Text = ""
        if self.event2 is not None:
            event2Text = " + {} x {}".format(self.multiplier2, self.event2)
        linkedRequirementText = ""
        if self.linkedRequirement is not None:
            linkedRequirementText = " - Linked with: {}".format(self.linkedRequirement.id)
        titleText = ""
        if self.title:
            titleText = " - " + self.title
            if not self.enableTitle:
                titleText += " (Title not used)"
        elif self.enableTitle:
            titleText = " - (Title is blank)"
        return "{}: {}{} - {} x {}{}{}{}".format(self.id, \
            self.candidateSemesterActive, titleText, \
            self.multiplier1, self.event1, event2Text, \
                linkedRequirementText, \
                "" if self.enable else " [Off]")

