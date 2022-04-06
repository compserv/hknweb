from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class OfficerPortalViewTests(CandidateViewTestsBase):
    def test_officer_portal_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:officer"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
