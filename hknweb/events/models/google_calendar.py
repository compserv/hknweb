from django.db import models

from hknweb.events.models.constants import ACCESS_LEVELS


class GoogleCalendarCredentials(models.Model):
    file = models.FileField()

    class Meta:
        verbose_name_plural = "GoogleCalendarCredentials"


class GCalAccessLevelMapping(models.Model):
    access_level = models.IntegerField(
        choices=ACCESS_LEVELS,
        default=0,
    )
    calendar_id = models.CharField(max_length=255)

    @staticmethod
    def get_calendar_id(access_level: int) -> str:
        mapping = GCalAccessLevelMapping.objects.filter(access_level=access_level).first()
        return mapping.calendar_id
