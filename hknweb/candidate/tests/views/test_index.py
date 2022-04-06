from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class IndexViewTests(CandidateViewTestsBase):
    def test_index_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:index"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
