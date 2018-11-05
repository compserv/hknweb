from django.db import models


max_strlen = 255


class Alumnus(models.Model):
    name_id         = models.IntegerField()
    first_name      = models.CharField(max_length=max_strlen)
    last_name       = models.CharField(max_length=max_strlen)
    perm_email      = models.EmailField()
    mailing_list    = models.BooleanField()
    grad_semester   = models.CharField(max_length=max_strlen)
    grad_school     = models.CharField(max_length=max_strlen)
    job_title       = models.CharField(max_length=max_strlen)
    company         = models.CharField(max_length=max_strlen)
    salary          = models.IntegerField()
    created_at      = models.DateTimeField()
    updated_at      = models.DateTimeField()
    location        = models.CharField(max_length=max_strlen)

    def generate_grad_semester(self, semester, year):
        return semester + ' ' + year

    def __str__(self):
        return self.perm_email