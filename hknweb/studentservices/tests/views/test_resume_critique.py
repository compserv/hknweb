from django.test import TestCase

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class ResumeCritiqueViewTests(TestCase):
    def test_resume_critique_submit_get(self):
        response = self.client.get(reverse("studentservices:resume"))

        self.assertEqual(response.status_code, 200)

    def test_resume_critique_submit_form_valid(self):
        document = SimpleUploadedFile("test_resume.pdf", b"file_content")
        data = {
            "name": "test_name",
            "document": document,
            "notes": "test_notes",
            "email": "test_email@email.com",
        }
        response = self.client.post(reverse("studentservices:resume"), data=data)

        self.assertEqual(response.status_code, 200)

    def test_resume_critique_submit_form_invalid(self):
        document = SimpleUploadedFile("test_resume.pdf", b"file_content")
        data = {
            "name": "test_name",
            "document": document,
            "notes": "test_notes",
            "email": "test_email",
        }
        response = self.client.post(reverse("studentservices:resume"), data=data)

        self.assertEqual(response.status_code, 200)
