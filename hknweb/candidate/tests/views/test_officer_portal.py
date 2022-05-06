from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase
from hknweb.candidate.tests.models.utils import ModelFactory


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

        logistics = ModelFactory.create_default_logistics()
        logistics.misc_reqs.add(ModelFactory.create_misc_req())
        logistics.save()

        response = self.client.get(reverse("candidate:officer_portal"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
