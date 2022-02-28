from django.db import models


class GoogleCalendarCredentials(models.Model):
    file = models.FileField()

    class Meta:
        verbose_name_plural = "GoogleCalendarCredentials"
