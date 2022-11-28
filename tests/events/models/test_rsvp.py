from django.test import TestCase

from tests.events.models.utils import ModelFactory


class RsvpModelTests(TestCase):
    def setUp(self):
        (
            event_create_user,
            rsvp_users,
            event_type,
            event_name,
            event,
            rsvps,
        ) = ModelFactory.create_event_with_rsvps()

        self.event_create_user = event_create_user
        self.rsvp_users = rsvp_users
        self.event_type = event_type
        self.event_name = event_name
        self.event = event
        self.rsvps = rsvps

    def test_repr(self):
        for rsvp, user in zip(self.rsvps, self.rsvp_users):
            expected = "Rsvp(event={}, user={})".format(self.event, user.username)
            actual = repr(rsvp)

            self.assertEqual(expected, actual)

    def test_str(self):
        for rsvp in self.rsvps:
            expected = self.event_name
            actual = str(rsvp)

            self.assertEqual(expected, actual)

    def test_has_not_rsvpd_user_not_rsvpd_returns_false(self):
        user_not_rsvpd = self.event_create_user
        rsvp = self.rsvps[0]

        self.assertTrue(rsvp.has_not_rsvpd(user_not_rsvpd, self.event))

    def test_has_not_rsvpd_user_rsvpd_returns_true(self):
        user_rsvpd = self.rsvp_users[0]
        rsvp = self.rsvps[0]

        self.assertFalse(rsvp.has_not_rsvpd(user_rsvpd, self.event))
