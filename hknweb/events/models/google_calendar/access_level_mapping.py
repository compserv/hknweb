from django.db import models

from hknweb.events.models.constants import ACCESS_LEVELS


class GCalAccessLevelMapping(models.Model):
    access_level = models.IntegerField(
        choices=ACCESS_LEVELS,
        default=0,
    )
    calendar_id = models.CharField(max_length=255)

    @staticmethod
    def get_calendar_id(access_level: int) -> str:
        mappings = GCalAccessLevelMapping.objects.filter(access_level=access_level)
        if not mappings.exists():
            return None

        mapping = mappings.first()
        return mapping.calendar_id
