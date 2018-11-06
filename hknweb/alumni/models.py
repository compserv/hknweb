from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
import os
from hknweb.settings.common import BASE_DIR


max_strlen = 255

FALL = 'Fall'
SPRING = 'Spring'
SUMMER = 'Summer'
SEASONS = ((FALL, "Fall"), (SPRING, "Spring"), (SUMMER, "Summer"))


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


with open(os.path.join(BASE_DIR, 'hknweb/alumni/static/countries_states.txt')) as f:
    COUNTRIES = f.read().splitlines()


class Alumnus(models.Model):
    id              = models.AutoField(primary_key=True)
    first_name      = models.CharField(max_length=max_strlen, default='')
    last_name       = models.CharField(max_length=max_strlen, default='')
    perm_email      = models.EmailField(default='', verbose_name="permanent email")
    mailing_list    = models.BooleanField(default='')
    grad_season     = models.CharField(max_length=2, choices=SEASONS, default=FALL, verbose_name="graduation season")
    grad_year       = models.IntegerField(validators=[MinValueValidator(1915), max_value_current_year],
                                          default=current_year(), verbose_name="graduation year")
    grad_school     = models.CharField(max_length=max_strlen, blank=True, default='')
    job_title       = models.CharField(max_length=max_strlen, blank=True, default='')
    company         = models.CharField(max_length=max_strlen, blank=True, default='')
    salary          = models.IntegerField(default=0)
    created_at      = models.DateTimeField(default=timezone.now)
    updated_at      = models.DateTimeField(default=timezone.now)
    city            = models.CharField(max_length=max_strlen, default='')
    country_state   = models.CharField(max_length=max_strlen, choices=[(c, c) for c in COUNTRIES],
                                       default='USA: CA', verbose_name="country or state")
    suggestions     = models.CharField(max_length=2000, blank=True, default='')

    @property
    def graduation_semester(self):
        return self.grad_season + ' ' + str(self.grad_year)

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.name
