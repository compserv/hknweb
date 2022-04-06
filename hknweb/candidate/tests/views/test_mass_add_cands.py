import json

from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

from hknweb.coursesemester.models import Semester
from hknweb.candidate.tests.views.utils import CandidateViewTestsBase


class MassAddCandidatesViewTests(CandidateViewTestsBase):
    def test_create_candidates_get_returns_200(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:create_candidates"))

        self.client.logout()

        self.assertEqual(response.status_code, 200)

    def test_create_candidates_get_returns_404(self):
        self.client.login(username=self.officer.username, password=self.password)

        response = self.client.get(reverse("candidate:add_cands"))

        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def test_create_candidates_missing_cand_csv_returns_false(self):
        self.client.login(username=self.officer.username, password=self.password)

        data = {}
        response = self.client.post(reverse("candidate:add_cands"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)["success"])

    def test_create_candidates_misnamed_cand_csv_returns_false(self):
        self.client.login(username=self.officer.username, password=self.password)

        cand_csv = SimpleUploadedFile(
            "csv_file.txt",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    "incorrect_user_email@berkeley.edu",
                    "incorrect_user_first_name",
                    "incorrect_user_last_name",
                )
            ),
        )
        data = {"cand_csv": cand_csv}
        response = self.client.post(reverse("candidate:add_cands"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)["success"])

    def test_create_candidates_returns_true(self):
        now = timezone.now()
        month = now.month
        if (1 <= month) and (month <= 5):
            sem = "Spring"
        elif (6 <= month) and (month < 8):
            sem = "Summer"
        elif (8 <= month) and (month <= 12):
            sem = "Fall"

        Semester.objects.create(semester=sem, year=now.year)
        settings.NO_THREADING = True

        self.client.login(username=self.officer.username, password=self.password)

        cand_csv = SimpleUploadedFile(
            "csv_file.csv",
            str.encode(
                "Email,First Name,Last Name\n{},{},{}\n".format(
                    "test_user_email@berkeley.edu",
                    "test_user_first_name",
                    "test_user_last_name",
                )
            ),
        )
        data = {"cand_csv": cand_csv}
        response = self.client.post(reverse("candidate:add_cands"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)["success"])

        kwargs = {"id": json.loads(response.content)["id"]}
        response = None
        while not response or not json.loads(response.content)["is_done"]:
            response = self.client.post(
                reverse("candidate:check_create_cand_status", kwargs=kwargs)
            )

        self.client.logout()

        self.assertTrue(json.loads(response.content)["is_successful"])
