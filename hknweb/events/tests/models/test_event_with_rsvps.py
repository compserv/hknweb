from django.test import TestCase

from hknweb.events.tests.models.utils import ModelFactory


class EventWithRsvpsTests(TestCase):
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

    def test_admitted_set(self):
        expected = self.rsvps[: self.event.rsvp_limit]
        actual = list(self.event.admitted_set())

        self.assertListEqual(expected, actual)

    def test_waitlist_set(self):
        expected = self.rsvps[self.event.rsvp_limit :]
        actual = list(self.event.waitlist_set())

        self.assertListEqual(expected, actual)

    def test_on_waitlist_user_not_on_waitlist_returns_false(self):
        user_not_on_waitlist = self.rsvp_users[0]
        self.assertFalse(self.event.on_waitlist(user_not_on_waitlist))

    def test_on_waitlist_user_on_waitlist_returns_true(self):
        user_on_waitlist = self.rsvp_users[self.event.rsvp_limit]
        self.assertTrue(self.event.on_waitlist(user_on_waitlist))

    def test_newly_off_waitlist_rsvps(self):
        old_admitted = set([self.rsvps[0], self.rsvps[2]])

        expected = set([self.rsvps[1]])
        actual = self.event.newly_off_waitlist_rsvps(old_admitted)

        self.assertSetEqual(expected, actual)
