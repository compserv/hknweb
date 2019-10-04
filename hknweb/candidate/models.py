from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

MAX_STRLEN = 85 # default max length for char fields
MAX_TXTLEN = 2000 # default max length for text fields


class OffChallenge(models.Model):
    """
    Model for an officer challenge submitted by a candidate.
    Each candidate who did the challenge must submit a separate request
    (May be changed in the future).
    Assumes the existence of two groups, "candidate" and "officer" (defined in common.py).
    """

    class Meta:
        verbose_name = "Officer challenge"

    requester       = models.ForeignKey('auth.User', limit_choices_to={'groups__name': settings.CAND_GROUP},
                        on_delete=models.CASCADE, default=None, related_name='requester')
    officer         = models.ForeignKey('auth.User', limit_choices_to={'groups__name': settings.OFFICER_GROUP},
                        on_delete=models.CASCADE, default=None, related_name='officer')
    name            = models.CharField(max_length=MAX_STRLEN, default='', verbose_name="title")
    description     = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # proof of completion is optional (if proof is a file, the candiate can send it to slack)
    proof           = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # optional comment about, say, why the confirmation request was declined
    officer_comment = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # whether officer reviewed this request
    reviewed        = models.BooleanField(default=False)
    # whether officer confirmed this request
    # if reviewed == True and confirmed == False, then officer declined request
    # if reviewed == False, then challenge is not confirmed no matter what the field confirmed equals
    confirmed       = models.BooleanField(default=False)
    request_date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# CS 61A LECTURE NUMBER 3141592653589793238462643383
class Announcement(models.Model):
    """
    Model for an announcement. Created by VP or some other superuser.
    Displayed on the candidate portal. The title will be displayed in bold,
    and the text will follow that in normal font, with a space in between.
    """

    title           = models.CharField(max_length=MAX_STRLEN, default='')
    text            = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # if visible == False, then admins can see announcement but it's not displayed on portal
    visible         = models.BooleanField(default=False)
    release_date    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title if self.title != '' else self.text

