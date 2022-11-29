from django.urls import reverse

from tests.candidate.views.utils import CandidateViewTestsBase


class AutocompleteViewTests(CandidateViewTestsBase):
    def test_autocomplete_officer_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:autocomplete_officer") + "?q=bob")

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_autocomplete_user_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:autocomplete_user") + "?q=bob")

        self.client.logout()

        self.assertEqual(response.status_code, 200)
