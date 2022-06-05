from typing import Any, Dict

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from hknweb.events.models.attendance.attendance_form import AttendanceForm
from hknweb.events.tests.models.utils import ModelFactory


class ManageAttendanceViewTests(TestCase):
    def setUp(self):
        user = ModelFactory.create_user()
        password = "custom password"
        user.set_password(password)
        user.save()

        content_type = ContentType.objects.get_for_model(AttendanceForm)
        permission = Permission.objects.get(
            content_type=content_type, codename="add_attendanceform"
        )
        user.user_permissions.add(permission)

        self.client.login(username=user.username, password=password)

        self.attendance_form = ModelFactory.create_attendanceform()

    def test_manage_attendance_post_returns_302(self):
        data: Dict[str, str] = {
            "secret_word": self.attendance_form.secret_word,
        }
        kwargs: Dict[str, Any] = {
            "event_id": self.attendance_form.event.id,
        }
        self.attendance_form.delete()

        url = reverse("events:manage_attendance", kwargs=kwargs)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)

    def test_manage_attendance_get_existing_returns_200(self):
        kwargs: Dict[str, Any] = {
            "event_id": self.attendance_form.event.id,
        }
        url = reverse("events:manage_attendance", kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
