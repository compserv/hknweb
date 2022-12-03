from datetime import datetime
from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester
from hknweb.events.models import EventType

from hknweb.candidate.models import (
    Announcement,
    BitByteActivity,
    OffChallenge,
    EventReq,
    Logistics,
    FormReq,
    MiscReq,
)


class ModelFactory:
    @staticmethod
    def create_user(**kwargs):
        default_kwargs = {
            "username": "default username",
        }
        kwargs = {**default_kwargs, **kwargs}
        return User.objects.create(**kwargs)

    @staticmethod
    def create_semester(semester, year, **kwargs):
        required_kwargs = {
            "semester": semester,
            "year": year,
        }
        kwargs = {
            **required_kwargs,
            **kwargs,
        }
        return Semester.objects.create(**kwargs)

    @staticmethod
    def create_eventtype(type, **kwargs):
        required_kwargs = {
            "type": type,
        }
        kwargs = {
            **required_kwargs,
            **kwargs,
        }
        return EventType.objects.create(**kwargs)

    @staticmethod
    def create_bitbyteactivity_activity(participants, **kwargs):
        default_kwargs = {
            "proof": "default proof",
            "notes": "default notes",
        }
        kwargs = {
            **default_kwargs,
            **kwargs,
        }
        bitbyteactivity = BitByteActivity.objects.create(**kwargs)

        bitbyteactivity.participants.add(*participants)
        bitbyteactivity.save()

        return bitbyteactivity

    @staticmethod
    def create_officerchallenge_activity(requester, officer, **kwargs):
        required_kwargs = {
            "requester": requester,
            "officer": officer,
        }
        default_kwargs = {
            "name": "default name",
            "proof": "default proof",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        }
        return OffChallenge.objects.create(**kwargs)

    @staticmethod
    def create_announcement(**kwargs):
        default_kwargs = {
            "title": "default title",
            "text": "default text",
        }
        kwargs = {
            **default_kwargs,
            **kwargs,
        }
        return Announcement.objects.create(**kwargs)

    @staticmethod
    def create_event_req(**kwargs):
        required_kwargs = {
            "n": 3,
        }
        kwargs = {
            **required_kwargs,
            **kwargs,
        }
        return EventReq.objects.create(**kwargs)

    @staticmethod
    def create_default_event_req(**kwargs):
        event_req = ModelFactory.create_event_req()
        event_req.event_types.add(ModelFactory.create_eventtype("test_event_type"))
        return event_req

    @staticmethod
    def create_default_logistics(**kwargs):
        logistics: Logistics = Logistics.objects.create(
            semester=ModelFactory.create_semester("Fa", 1990),
            date_start=datetime.now(),
            date_end=datetime.now(),
            min_challenges=1,
            min_hangouts=1,
            num_interactivities=3,
            num_bitbyte=3,
        )

        logistics.event_reqs.add(ModelFactory.create_default_event_req())

        return logistics

    @staticmethod
    def create_misc_req(**kwargs):
        required_kwargs = {
            "title": "test_title",
            "description": "test_description",
            "due_date": "test_due_date",
        }
        kwargs = {
            **required_kwargs,
            **kwargs,
        }
        return MiscReq.objects.create(**kwargs)

    @staticmethod
    def create_form_req(**kwargs):
        required_kwargs = {
            "title": "test_title",
            "link": "test_description",
            "due_date": "test_due_date",
        }
        kwargs = {
            **required_kwargs,
            **kwargs,
        }
        return FormReq.objects.create(**kwargs)
