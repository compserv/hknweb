from django.urls import reverse

from hknweb.candidate.models import OffChallenge

from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class ChallengeConfirmViewTests(CandidateViewTestsBase):
    def test_challenge_confirm_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id}
        response = self.client.get(reverse("candidate:challengeconfirm", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_challenge_confirm_post_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id}
        data = {"officer_confirmed": True}
        response = self.client.post(reverse("candidate:challengeconfirm", kwargs=kwargs), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_challenge_confirm_same_id_returns_403(self):
        self.client.login(username=self.officer2.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id}
        data = {"officer_confirmed": True}
        response = self.client.post(reverse("candidate:challengeconfirm", kwargs=kwargs), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 403)

    def test_challenge_confirm_post_confirmed_sends_true_email(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )
        oc.csec_confirmed = True
        oc.save()

        kwargs = {"pk": oc.id}
        data = {"officer_confirmed": True}
        response = self.client.post(reverse("candidate:challengeconfirm", kwargs=kwargs), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_challenge_confirm_post_not_confirmed_sends_false_email(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )
        oc.csec_confirmed = True
        oc.save()

        kwargs = {"pk": oc.id}
        data = {"officer_confirmed": False}
        response = self.client.post(reverse("candidate:challengeconfirm", kwargs=kwargs), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_confirm_get_returns_404(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"id": oc.id}
        response = self.client.get(reverse("candidate:confirm", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def test_confirm_post_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"id": oc.id}
        response = self.client.post(reverse("candidate:confirm", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_officer_review_confirmation_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id}
        response = self.client.get(reverse("candidate:reviewconfirm", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
