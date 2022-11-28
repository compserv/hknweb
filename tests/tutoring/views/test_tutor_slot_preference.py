from django.urls import reverse

from tests.candidate.views.utils import CandidateViewTestsBase


class TutorSlotPreferenceViewTests(CandidateViewTestsBase):
    def test_tutor_slot_preference_missing_tutor_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("tutoring:slotpref"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_tutor_slot_preference_existing_tutor_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("tutoring:slotpref"))
        response = self.client.get(reverse("tutoring:slotpref"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_tutor_slot_preference_post_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.post(reverse("tutoring:slotpref"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
