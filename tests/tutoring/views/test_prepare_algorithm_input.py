from django.urls import reverse

from tests.candidate.views.utils import CandidateViewTestsBase


class PrepareAlgorithmInputViewTests(CandidateViewTestsBase):
    def test_prepare_algorithm_input_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.post(reverse("tutoring:coursepref"))
        response = self.client.post(reverse("tutoring:slotpref"))
        response = self.client.get(reverse("tutoring:prepare-algorithm-input"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
