from django.urls import reverse

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class ViewByUsernameViewTests(CandidateViewTestsBase):
    def test_view_by_username_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        kwargs = {"username": self.officer.username}
        response = self.client.get(reverse("candidate:viewcand", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_view_by_username_get_missing_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        kwargs = {"username": "bob"}
        response = self.client.get(reverse("candidate:viewcand", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 302)
