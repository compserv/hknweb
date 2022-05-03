from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class CandidatePortalViewTests(CandidateViewTestsBase):
    def test_index_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:candidate_portal"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
