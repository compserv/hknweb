from django.urls import reverse

from hknweb.candidate.models import OffChallenge

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class ChallengeRequestViewTests(CandidateViewTestsBase):
    def test_challenge_request_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:candrequests"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_challenge_request_post_returns_302(self):
        self.client.login(username=self.candidate.username, password=self.password)

        data = {
            "name": "test_name",
            "officer": self.officer.id,
        }
        response = self.client.post(reverse("candidate:candrequests"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)
