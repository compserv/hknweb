from django.db import models
from django.utils import timezone


max_strlen = 255


class Alumnus(models.Model):
    id              = models.AutoField(primary_key=True)
    first_name      = models.CharField(max_length=max_strlen, default='')
    last_name       = models.CharField(max_length=max_strlen, default='')
    perm_email      = models.EmailField(default='')
    mailing_list    = models.BooleanField(default='')
    grad_semester   = models.CharField(max_length=max_strlen, default='')
    grad_school     = models.CharField(max_length=max_strlen, default='')
    job_title       = models.CharField(max_length=max_strlen, default='')
    company         = models.CharField(max_length=max_strlen, default='')
    salary          = models.IntegerField(default=-1)
    created_at      = models.DateTimeField(default=timezone.now)
    updated_at      = models.DateTimeField(default=timezone.now)
    location        = models.CharField(max_length=max_strlen, default='')
    suggestions     = models.CharField(max_length=2000, default='')

    def generate_grad_semester(self, semester, year):
        return semester + ' ' + year

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.name
