from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class CandidatePortalViewTests(CandidateViewTestsBase):
    def test_candidate_portal_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        response = self.client.get(reverse("candidate:candidate_portal"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_candidate_portal_view_by_username_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        kwargs = {"username": self.officer.username}
        response = self.client.get(
            reverse("candidate:candidate_portal_view_by_username", kwargs=kwargs)
        )

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_candidate_portal_view_by_username_get_missing_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        kwargs = {"username": "bob"}
        response = self.client.get(
            reverse("candidate:candidate_portal_view_by_username", kwargs=kwargs)
        )

        self.client.logout()

        self.assertEqual(response.status_code, 302)
