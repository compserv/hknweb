from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class AutocompleteViewTests(CandidateViewTestsBase):
    def test_candreq_autocomplete_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:candreq/autocomplete") + "?q=bob")

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_bitbyte_autocomplete_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:bitbyte/autocomplete") + "?q=bob")

        self.client.logout()

        self.assertEqual(response.status_code, 200)
