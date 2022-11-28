from django.urls import reverse

from tests.candidate.views.utils import CandidateViewTestsBase


class TutorCoursePreferenceViewTests(CandidateViewTestsBase):
    def test_tutor_course_preference_missing_tutor_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("tutoring:coursepref"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_tutor_course_preference_existing_tutor_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("tutoring:coursepref"))
        response = self.client.get(reverse("tutoring:coursepref"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_tutor_course_preference_post_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.post(reverse("tutoring:coursepref"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
