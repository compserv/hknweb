from django.test import TestCase

from django.urls import reverse


class ResumeCritiqueViewTests(TestCase):
    def test_resume_critique_submit_get(self):
        response = self.client.get(reverse("studentservices:resume"))

        self.assertEqual(response.status_code, 200)

    def test_resume_critique_submit_form_valid(self):
        data = {
            "name": "test_name",
            "document": "test_document",
            "notes": "test_notes",
            "email": "test_email@email.com",
        }
        response = self.client.post(reverse("studentservices:resume"), data=data)

        self.assertEqual(response.status_code, 200)

    def test_resume_critique_submit_form_invalid(self):
        data = {
            "name": "test_name",
            "document": "test_document",
            "notes": "test_notes",
            "email": "test_email",
        }
        response = self.client.post(reverse("studentservices:resume"), data=data)

        self.assertEqual(response.status_code, 200)
