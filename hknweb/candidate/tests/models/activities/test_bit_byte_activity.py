from django.test import TestCase

from hknweb.candidate.models import BitByteActivity

from hknweb.candidate.tests.models.utils import ModelFactory


class BitByteActivityActivityModelTests(TestCase):
    def setUp(self):
        user = ModelFactory.create_user()
        participants = [user]
        bitbyteactivity = ModelFactory.create_bitbyteactivity_activity(participants)

        self.user = user
        self.participants = participants
        self.bitbyteactivity = bitbyteactivity

    def test_str(self):
        expected = ", ".join([c.username for c in self.participants]) + "; " + self.bitbyteactivity.proof
        actual = str(self.bitbyteactivity)

        self.assertEqual(expected, actual)

    def test_is_confirmed_returns_true_when_confirmed(self):
        self.bitbyteactivity.confirmed = True
        self.bitbyteactivity.save()

        self.assertTrue(BitByteActivity.objects.get(id=self.bitbyteactivity.id).is_confirmed)

    def test_is_confirmed_returns_false_when_not_confirmed(self):
        self.bitbyteactivity.confirmed = False
        self.bitbyteactivity.save()

        self.assertFalse(BitByteActivity.objects.get(id=self.bitbyteactivity.id).is_confirmed)

    def test_is_rejected_returns_false_when_confirmed(self):
        self.bitbyteactivity.confirmed = True
        self.bitbyteactivity.save()

        self.assertFalse(BitByteActivity.objects.get(id=self.bitbyteactivity.id).is_rejected)

    def test_is_rejected_returns_true_when_not_confirmed(self):
        self.bitbyteactivity.confirmed = False
        self.bitbyteactivity.save()

        self.assertTrue(BitByteActivity.objects.get(id=self.bitbyteactivity.id).is_rejected)
