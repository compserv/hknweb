from typing import Any, Dict

from django.test import TestCase
from django.urls import reverse

from hknweb.events.tests.models.utils import ModelFactory
from hknweb.events.tests.views.rsvp_transactions.utils import setUp


class ManageAttendanceViewTests(TestCase):
    def setUp(self):
        setUp(self, ["change_rsvp"])

        self.rsvp = ModelFactory.create_rsvp(self.user, self.event)

        self.attendance_form = ModelFactory.create_attendanceform()

    def test_manage_attendance_post_returns_302(self):
        data: Dict[str, str] = {
            "secret_word": self.attendance_form.secret_word,
        }
        kwargs: Dict[str, Any] = {
            "event_id": self.attendance_form.event.id,
            "attendance_form_id": self.attendance_form.id,
            "rsvp_id": self.rsvp.id,
        }

        url = reverse("events:submit_attendance", kwargs=kwargs)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)

    def test_manage_attendance_get_returns_200(self):
        kwargs: Dict[str, Any] = {
            "event_id": self.attendance_form.event.id,
            "attendance_form_id": self.attendance_form.id,
            "rsvp_id": self.rsvp.id,
        }

        url = reverse("events:submit_attendance", kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
