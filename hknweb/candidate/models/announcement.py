from django.db import models
from django.utils import timezone

from hknweb.candidate.models.constants import MAX_STRLEN, MAX_TXTLEN


class Announcement(models.Model):
    """
    Model for an announcement. Created by VP or some other superuser.
    Displayed on the home page. The title will be displayed in bold,
    and the text will follow that in normal font, with a space in between.
    """

    title = models.CharField(max_length=MAX_STRLEN, default="")
    text = models.TextField(max_length=MAX_TXTLEN, blank=True, default="")
    # if visible == False, then admins can see announcement but it's not displayed on portal
    visible = models.BooleanField(default=False)
    release_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title if self.title != "" else self.text
