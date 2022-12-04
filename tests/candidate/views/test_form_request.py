from django.urls import reverse

from tests.candidate.views.utils import CandidateViewTestsBase


class FormRequestViewTests(CandidateViewTestsBase):
    def test_request_bitbyte_get_returns_404(self):
        self.client.login(username=self.candidate.username, password=self.password)

        data = {
            "participants": [self.candidate.id],
            "proof": "test_proof",
        }
        response = self.client.get(reverse("candidate:request_bitbyte"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def test_request_bitbyte_badrequest_returns_400(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.post(reverse("candidate:request_bitbyte"))

        self.client.logout()

        self.assertEqual(response.status_code, 400)

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
