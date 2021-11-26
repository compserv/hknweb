from django.test import TestCase

from hknweb.events.tests.models.utils import ModelFactory


class RsvpModelTests(TestCase):
    def setUp(self):
        event_create_user = ModelFactory.create_user(username="event create user")
        num_rsvps = 3
        rsvp_users = [ModelFactory.create_user(username="rsvp_user_{}".format(str(i))) for i in range(1, 1 + num_rsvps)]

        event_type = ModelFactory.create_event_type()
        event_name = "custom event name"

        event = ModelFactory.create_event(
            name=event_name,
            event_type=event_type,
            created_by=event_create_user,
            rsvp_limit=num_rsvps - 1,
        )

        rsvps = [ModelFactory.create_rsvp(rsvp_user, event) for rsvp_user in rsvp_users]

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
