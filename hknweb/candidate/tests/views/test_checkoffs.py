from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

from hknweb.candidate.models import DuePayment
from hknweb.candidate.tests.views.utils import CandidateViewTestsBase
from hknweb.events.tests.models.utils import ModelFactory


class CheckoffViewTests(CandidateViewTestsBase):
    def test_checkoff_get_returns_404(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:checkoff_csv"))

        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def test_checkoff_invalid_csv_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.post(reverse("candidate:checkoff_csv"))

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_invalid_email_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv", b"Email,First Name,Last Name\nbob,bob,joe\n"
        )
        data = {"csv_file": csv_file}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_user_not_found_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    "incorrect_user_email@berkeley.edu",
                    "incorrect_user_first_name",
                    "incorrect_user_last_name",
                )
            ),
        )
        data = {"csv_file": csv_file}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_type_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    self.officer.email,
                    self.officer.first_name,
                    self.officer.last_name,
                )
            ),
        )
        data = {"csv_file": csv_file, "checkoff_type": ""}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_event_doesnt_exist_returns_302(self):
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    self.officer.email,
                    self.officer.first_name,
                    self.officer.last_name,
                )
            ),
        )
        data = {"csv_file": csv_file, "checkoff_type": "event", "event_id": -1}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_event_returns_302(self):
        event_type = ModelFactory.create_event_type(type="test_event_type")
        event = ModelFactory.create_event(
            "test_event_name", event_type, created_by=self.officer
        )
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    self.officer.email,
                    self.officer.first_name,
                    self.officer.last_name,
                )
            ),
        )
        data = {"csv_file": csv_file, "checkoff_type": "event", "event_id": event.id}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_requirement_id_missing_returns_302(self):
        dp = DuePayment.objects.create()
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    self.officer.email,
                    self.officer.first_name,
                    self.officer.last_name,
                )
            ),
        )
        data = {"csv_file": csv_file, "checkoff_type": "dues"}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_checkoff_requirement_returns_302(self):
        dp = DuePayment.objects.create()
        self.client.login(username=self.officer.username, password=self.password)

        csv_file = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    self.officer.email,
                    self.officer.first_name,
                    self.officer.last_name,
                )
            ),
        )
        data = {"csv_file": csv_file, "checkoff_type": "dues", "dues_selection": dp.id}
        response = self.client.post(reverse("candidate:checkoff_csv"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 302)

    def test_member_checkoff_view_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:checkoff"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)
