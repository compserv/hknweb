from django.urls import reverse

from tests.candidate.views.utils import CandidateViewTestsBase
from tests.candidate.models.utils import ModelFactory
from tests.events.models.utils import ModelFactory as EventsModelFactory


class OfficerPortalViewTests(CandidateViewTestsBase):
    def test_officer_portal_no_logistics_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:officer_portal"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_officer_portal_with_logistics_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        ModelFactory.create_bitbyteactivity_activity([self.candidate])
        ModelFactory.create_officerchallenge_activity(self.candidate, self.officer)
        event = EventsModelFactory.create_event_with_rsvps()[4]

        logistics = ModelFactory.create_default_logistics()
        logistics.misc_reqs.add(ModelFactory.create_misc_req())
        logistics.mandatory_events.add(event)
        logistics.save()

        response = self.client.get(reverse("candidate:officer_portal"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_officer_portal_with_completed_reqs_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        ModelFactory.create_bitbyteactivity_activity([self.candidate])
        ModelFactory.create_officerchallenge_activity(self.candidate, self.officer)

        _, _, _, _, event, _ = EventsModelFactory.create_event_with_rsvps()
        rsvp = EventsModelFactory.create_rsvp(self.candidate, event)
        rsvp.confirmed = True
        rsvp.save()

        misc_req = ModelFactory.create_misc_req()
        misc_req.completed.add()

        logistics = ModelFactory.create_default_logistics()
        logistics.misc_reqs.add(misc_req)
        logistics.mandatory_events.add(event)
        logistics.save()

        response = self.client.get(reverse("candidate:officer_portal"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
