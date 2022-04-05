import json
import time

from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

from hknweb.thread.models import ThreadTask
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
            str.encode("Email,First Name,Last Name\n{},{},{}\n".format(
                "incorrect_user_email@berkeley.edu",
                "incorrect_user_first_name",
                "incorrect_user_last_name",
            ))
        )
        data = {"cand_csv": cand_csv}
        response = self.client.post(reverse("candidate:add_cands"), data=data)

        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)["success"])
