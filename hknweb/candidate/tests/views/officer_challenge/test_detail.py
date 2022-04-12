from django.urls import reverse

from hknweb.candidate.models import OffChallenge

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class ChallengeDetailViewTests(CandidateViewTestsBase):
    def test_challenge_detail_get_returns_200(self):
        self.client.login(username=self.candidate.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id}
        response = self.client.get(reverse("candidate:detail", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_challenge_detail_get_officer_view_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id}
        response = self.client.get(reverse("candidate:detail", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
