from django.contrib.auth.models import User

from hknweb.candidate.models import BitByteActivity, OffChallenge


class ModelFactory:
    @staticmethod
    def create_user(**kwargs):
        default_kwargs = {
            "username": "default username",
        }
        kwargs = {**default_kwargs, **kwargs}
        return User.objects.create(**kwargs)

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
