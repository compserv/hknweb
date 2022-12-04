from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from hknweb.candidate.models import BitByteActivity
from hknweb.candidate.admin import BitByteActivityAdmin

from tests.candidate.models.utils import ModelFactory


class BitByteActivityActivityModelTests(TestCase):
    def setUp(self):
        user = ModelFactory.create_user()
        participants = [user]
        bitbyteactivity = ModelFactory.create_bitbyteactivity_activity(participants)
        bitbyteactivity_admin = BitByteActivityAdmin(model=BitByteActivity, admin_site=AdminSite())

        self.user = user
        self.participants = participants
        self.bitbyteactivity = bitbyteactivity
        self.bitbyteactivity_admin = bitbyteactivity_admin

    def test_participant_usernames(self):
        expected = ", ".join([c.username for c in self.participants])
        actual = self.bitbyteactivity_admin.participant_usernames(self.bitbyteactivity)

        self.assertEqual(expected, actual)
