from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class BitByteViewTests(CandidateViewTestsBase):
    def test_bitbyte_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:bitbyte"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_bitbyte_submit_returns_302(self):
        self.client.login(username=self.candidate.username, password=self.password)

        data = {
            "participants": [self.candidate.id],
            "proof": "test_proof",
        }
        response = self.client.post(reverse("candidate:bitbyte"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)
