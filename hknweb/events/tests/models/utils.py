import datetime

from django.utils import timezone

from django.contrib.auth.models import User
from hknweb.events.models import Event, EventType


class ModelFactory:
    @staticmethod
    def create_user(**kwargs):
        default_kwargs = {
            "username": "default username",
        }
        return User.objects.create(**default_kwargs, **kwargs)

    @staticmethod
    def create_event_type(**kwargs):
        default_kwargs = {
            "type": "default event type",
        }
        return EventType.objects.create(**default_kwargs, **kwargs)

    @staticmethod
    def create_event(name, event_type, created_by, **kwargs):
        required_kwargs = {
            "name": name,
            "event_type": event_type,
            "created_by": created_by,
        }
        default_kwargs = {
            "slug": name,
            "start_time": timezone.now(),
            "end_time": timezone.now() + datetime.timedelta(hours=2),
            "location": "default location",
            "description": "default description",
        }
        return Event.objects.create(
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        )
