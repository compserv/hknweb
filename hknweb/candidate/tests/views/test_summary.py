from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class SummaryViewTests(CandidateViewTestsBase):
    def test_summary_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:summary"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
