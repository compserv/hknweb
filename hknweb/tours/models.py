from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.contrib.admin.widgets import AdminDateWidget

MAX_STRLEN = 255 # default max length for char fields
MAX_TXTLEN = 2000 # default max length for text fields

#.save adds to database
# POST user submits
#GET user wants something
class DepTour(models.Model):
    """
    Model for a department tour
    """

    class Meta:
        verbose_name = "Department Tour"

    name            = models.CharField(max_length=MAX_STRLEN, default='')
    email           = models.EmailField(max_length=MAX_STRLEN, default='')
    desired_time    = models.TimeField(verbose_name='Desired Time')
    date            = models.DateField(default=timezone.now,verbose_name='Desired Date')
    phone           = models.CharField(max_length=12, default='')
    comments        = models.TextField(max_length=MAX_TXTLEN, blank=True, default='', verbose_name='Additional comments')
    date_submitted  = models.DateTimeField(default=timezone.datetime.now)
    confirmed       = models.BooleanField(default=False)
    deprel_comments   = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')

    def __str__(self):
        return self.name
