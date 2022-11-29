from django.urls import reverse

from hknweb.candidate.models import OffChallenge, BitByteActivity

from tests.candidate.views.utils import CandidateViewTestsBase
from tests.candidate.models.utils import ModelFactory


class ConfirmRequestViewTests(CandidateViewTestsBase):
    def test_confirm_challenge_get_returns_404(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id, "action": 0}
        response = self.client.get(
            reverse("candidate:confirm_challenge", kwargs=kwargs)
        )

        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def test_confirm_challenge_post_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        oc = OffChallenge.objects.create(
            requester=self.candidate,
            officer=self.officer,
        )

        kwargs = {"pk": oc.id, "action": 0}
        response = self.client.post(
            reverse("candidate:confirm_challenge", kwargs=kwargs)
        )

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_confirm_bitbyte_get_returns_404(self):
        self.client.login(username=self.officer.username, password=self.password)

        bb = BitByteActivity.objects.create()
        bb.participants.add(self.candidate)
        bb.save()

        kwargs = {"pk": bb.id, "action": 0}
        response = self.client.get(reverse("candidate:confirm_bitbyte", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def test_confirm_bitbyte_post_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        bb = BitByteActivity.objects.create()
        bb.participants.add(self.candidate)
        bb.save()

        kwargs = {"pk": bb.id, "action": 0}
        response = self.client.post(reverse("candidate:confirm_bitbyte", kwargs=kwargs))

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_req_post_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        logistics = ModelFactory.create_default_logistics()
        misc_req = ModelFactory.create_misc_req()
        logistics.misc_reqs.add(misc_req)
        logistics.save()

        data = {
            "logistics_id": logistics.id,
            "type": "misc_req",
            "obj_title": misc_req.title,
            "user_id": self.candidate.id,
            "operation": "0",
        }
        response = self.client.post(reverse("candidate:checkoff_req"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 200)
