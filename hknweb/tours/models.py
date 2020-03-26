from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
from django.core.validators import RegexValidator

MAX_STRLEN = 255 
MAX_TXTLEN = 2000 

class DepTour(models.Model):
    """
    Model for a department tour
    """

    class Meta:
        verbose_name = "Department Tour"

    name            = models.CharField(max_length=MAX_STRLEN, default='')
    email           = models.EmailField(max_length=MAX_STRLEN, default='')
    desired_time    = models.TimeField(verbose_name='Desired Time')
    date            = models.DateField(default=datetime.date.today,verbose_name='Desired Date')
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{10}$', message="Enter a valid 10-digit phone number in the format: '9876543210'")
    phone           = models.CharField(validators=[phone_regex], max_length=15, default='')
    comments        = models.TextField(max_length=MAX_TXTLEN, blank=True, default='', verbose_name='Additional comments')
    date_submitted  = models.DateTimeField(default=timezone.datetime.now)
    confirmed       = models.BooleanField(default=False)
    deprel_comments = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')

    def __str__(self):
        return self.name
