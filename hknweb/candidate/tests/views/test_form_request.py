from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class FormRequestViewTests(CandidateViewTestsBase):
    def test_request_bitbyte_returns_302(self):
        self.client.login(username=self.candidate.username, password=self.password)

        data = {
            "participants": [self.candidate.id],
            "proof": "test_proof",
        }
        response = self.client.post(reverse("candidate:request_bitbyte"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_request_challenge_returns_302(self):
        self.client.login(username=self.candidate.username, password=self.password)

        data = {
            "officer": [self.officer.id],
            "name": "test_name",
            "proof": "test_proof",
        }
        response = self.client.post(reverse("candidate:request_challenge"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)
