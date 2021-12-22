import datetime

from django.utils import timezone

from django.contrib.auth.models import User
from hknweb.events.models import Event, EventType, Rsvp


class ModelFactory:
    @staticmethod
    def create_user(**kwargs):
        default_kwargs = {
            "username": "default username",
        }
        kwargs = {**default_kwargs, **kwargs}
        return User.objects.create(**kwargs)

    @staticmethod
    def create_event_type(**kwargs):
        default_kwargs = {
            "type": "default event type",
        }
        kwargs = {**default_kwargs, **kwargs}
        return EventType.objects.create(**kwargs)

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
        kwargs = {**required_kwargs, **default_kwargs, **kwargs}
        return Event.objects.create(**kwargs)

    @staticmethod
    def create_rsvp(user, event, **kwargs):
        required_kwargs = {
            "user": user,
            "event": event,
        }
        kwargs = {**required_kwargs, **kwargs}
        return Rsvp.objects.create(**kwargs)

    @staticmethod
    def create_event_with_rsvps():
        event_create_user = ModelFactory.create_user(username="event create user")
        num_rsvps = 3
        rsvp_users = [
            ModelFactory.create_user(username="rsvp_user_{}".format(str(i)))
            for i in range(1, 1 + num_rsvps)
        ]

        event_type = ModelFactory.create_event_type()
        event_name = "custom event name"

        event = ModelFactory.create_event(
            name=event_name,
            event_type=event_type,
            created_by=event_create_user,
            rsvp_limit=num_rsvps - 1,
        )

        rsvps = [ModelFactory.create_rsvp(rsvp_user, event) for rsvp_user in rsvp_users]

        return (
            event_create_user,
            rsvp_users,
            event_type,
            event_name,
            event,
            rsvps,
        )
