from django.test import TestCase

from django.urls import reverse

from hknweb import settings
from hknweb.models import DriveFolderID
from tests.candidate.models.utils import ModelFactory
from django.contrib.auth.models import Group, AnonymousUser

from hknweb.tutoring.models import CribSheet
from hknweb.coursesemester.models import Semester
from hknweb.google_drive_utils import create_pdf, create_folder
from hknweb.studentservices.models import CourseDescription
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


class CribViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.anon = AnonymousUser()
        cls.tutoring_officer = ModelFactory.create_user(username="tutoring_officer")
        cls.member = ModelFactory.create_user(username="member")
        cls.tutoring_group = Group.objects.create(name=settings.TUTORING_GROUP)
        cls.tutoring_officer.groups.add(cls.tutoring_group)
        
        cls.users = [(cls.anon, 302), (cls.member, 403), (cls.tutoring_officer, 200)]
    
    
    def test_crib_view_get(self):
        for user, status_code in self.users:
            self.client.force_login(user) if user.is_authenticated else self.client.logout()
            response = self.client.get(reverse("tutoring:crib"))
            self.assertEqual(response.status_code, status_code)
            if status_code == 200:
                self.assertTemplateUsed(response, "tutoring/crib.html")
                
    def test_crib_view_get_query(self):
        CourseDescription.objects.create(title="CS161", slug="cs161")
        Semester.objects.create(semester="Spring", year=2026)
        CribSheet.objects.create(
            course=CourseDescription.objects.get(title="CS161"),
            semester=Semester.objects.get(semester="Spring", year=2026),
            title="Test Sheet",
        )
        
        for user, status_code in self.users:
            self.client.force_login(user) if user.is_authenticated else self.client.logout()
            response = self.client.get(reverse("tutoring:crib"), {'q': 'test', 'course': 'CS161', 'semester': 'Spring 2026'})
            self.assertEqual(response.status_code, status_code)
            if status_code == 200:
                self.assertTemplateUsed(response, "tutoring/crib.html")
            
    def test_crib_view_post_empty_form(self):
        self.client.force_login(self.tutoring_officer)
        response = self.client.post(reverse("tutoring:crib"), {})
        
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tutoring/crib.html")
        
        
        
    @patch("hknweb.tutoring.views.crib.create_pdf")
    @patch("hknweb.tutoring.views.crib.create_folder")
    def test_crib_view_post_valid_form(self, mock_create_folder, mock_create_pdf):
        self.client.force_login(self.tutoring_officer)

        course = CourseDescription.objects.create(title="CS161", slug="cs161")
        Semester.objects.create(semester="Spring", year=2026)
        DriveFolderID.objects.create(title="Crib Sheets",folderID="test_folder_id")

        mock_create_pdf.return_value = {"status": True, "result": "test_pdf_id"}
        mock_create_folder.return_value = {"status": True, "result": "test_folder_id"}

        
        valid_file = SimpleUploadedFile(
            "test_crib.pdf",
            b"%PDF-1.4 test pdf content",
            content_type="application/pdf",
        )

        valid_data = {
            "course": course.pk,
            "title": "Test Sheet",
            "file": valid_file,
        }


        response = self.client.post(
            reverse("tutoring:crib"),
            data=valid_data,
            files={"file": valid_file},
        )
        

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tutoring/crib.html")
        self.assertTrue(CribSheet.objects.filter(title="Test Sheet", course=course).exists())     
        mock_create_folder.assert_called_once()
        course.refresh_from_db()
