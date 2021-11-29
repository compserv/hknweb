from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester
from hknweb.events.models import EventType

from hknweb.candidate.models import (
    Announcement,
    BitByteActivity,
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
    RequirementMandatory,
    OffChallenge,
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
            "description": "default description",
            "proof": "default proof",
            "officer_comment": "default officer_comment",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        }
        return OffChallenge.objects.create(**kwargs)

    @staticmethod
    def create_candidateform_requirement(**kwargs):
        default_kwargs = {
            "name": "default name",
        }
        kwargs = {
            **default_kwargs,
            **kwargs,
        }
        return CandidateForm.objects.create(**kwargs)

    @staticmethod
    def create_candidateformdoneentry_requirement(form, **kwargs):
        required_kwargs = {
            "form": form,
        }
        default_kwargs = {
            "notes": "default notes",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs
        }
        return CandidateFormDoneEntry.objects.create(**kwargs)

    @staticmethod
    def create_committeeproject_requirement(**kwargs):
        default_kwargs = {
            "name": "default name",
            "instructions": "default instructions",
        }
        kwargs = {
            **default_kwargs,
            **kwargs,
        }
        return CommitteeProject.objects.create(**kwargs)

    @staticmethod
    def create_committeeprojectdoneentry_requirement(committeeProject, **kwargs):
        required_kwargs = {
            "committeeProject": committeeProject,
        }
        default_kwargs = {
            "notes": "default notes",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs
        }
        return CommitteeProjectDoneEntry.objects.create(**kwargs)

    @staticmethod
    def create_duepayment_requirement(**kwargs):
        default_kwargs = {
            "name": "default name",
            "instructions": "default instructions",
        }
        kwargs = {
            **default_kwargs,
            **kwargs,
        }
        return DuePayment.objects.create(**kwargs)

    @staticmethod
    def create_duepaymentpaidentry_requirement(duePayment, **kwargs):
        required_kwargs = {
            "duePayment": duePayment,
        }
        default_kwargs = {
            "notes": "default notes",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs
        }
        return DuePaymentPaidEntry.objects.create(**kwargs)

    @staticmethod
    def create_bitbyteactivity_requirement(**kwargs):
        return RequirementBitByteActivity.objects.create(**kwargs)

    @staticmethod
    def create_event_requirement(eventType, **kwargs):
        required_kwargs = {
            "eventType": eventType,
        }
        default_kwargs = {
            "title": "default title",
        }
        kwargs = {
            **required_kwargs,
            **default_kwargs,
            **kwargs,
        }
        return RequriementEvent.objects.create(**kwargs)

    @staticmethod
    def create_hangout_requirement(**kwargs):
        default_kwargs = {
            "eventType": "officer_hangout",
        }
        kwargs = {
            **default_kwargs,
            **kwargs,
        }
        return RequirementHangout.objects.create(**kwargs)

    @staticmethod
    def create_mandatory_requirement(**kwargs):
        return RequirementMandatory.objects.create(**kwargs)

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
