from django.test import TestCase

from django.contrib.auth.models import Group

from hknweb.candidate.models import OffChallenge

from hknweb.candidate.tests.models.utils import ModelFactory


class OfficerChallengeActivityModelTests(TestCase):
    def setUp(self):
        requester = ModelFactory.create_user(username="requester")
        officer = ModelFactory.create_user(username="officer")

        group = Group(name="officer")
        group.save()
        group.user_set.add(officer)
        group.save()

        officer_challenge = ModelFactory.create_officerchallenge_activity(
            requester, officer
        )

        self.requester = requester
        self.officer = officer
        self.officer_challenge = officer_challenge

    def test_str(self):
        expected = self.officer_challenge.name
        actual = str(self.officer_challenge)

        self.assertEqual(expected, actual)

    def test_confirmed_returns_true(self):
        self.officer_challenge.officer_confirmed = True
        self.officer_challenge.save()

        self.assertTrue(
            OffChallenge.objects.get(id=self.officer_challenge.id).confirmed
        )

    def test_confirmed_returns_false(self):
        self.officer_challenge.officer_confirmed = False
        self.officer_challenge.save()

        self.assertFalse(
            OffChallenge.objects.get(id=self.officer_challenge.id).confirmed
        )

    def test_rejected_returns_false(self):
        self.officer_challenge.officer_confirmed = True
        self.officer_challenge.save()

        self.assertFalse(
            OffChallenge.objects.get(id=self.officer_challenge.id).rejected
        )

    def test_rejected_returns_true(self):
        self.officer_challenge.officer_confirmed = False
        self.officer_challenge.save()

        self.assertTrue(OffChallenge.objects.get(id=self.officer_challenge.id).rejected)
