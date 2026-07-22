import io

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from hknweb.forms import ProvisionCandidatesForm


def _make_csv_upload(rows):
    """Build an in-memory CSV upload matching the form's required columns.

    ``rows`` is a list of (first_name, last_name, email) tuples.
    """
    buffer = io.StringIO()
    buffer.write("First name,Last name,Berkeley email\r\n")
    for first_name, last_name, email in rows:
        buffer.write(f"{first_name},{last_name},{email}\r\n")

    return SimpleUploadedFile(
        "candidates.csv",
        buffer.getvalue().encode("utf-8"),
        content_type="text/csv",
    )


class ProvisionCandidatesFormTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name=settings.CAND_GROUP)

    def test_duplicate_emails_within_same_batch_differing_only_in_case(self):
        # Two rows for the "same" candidate whose email only differs by case.
        # Only one account should be created, and the form should not raise.
        upload = _make_csv_upload(
            [
                ("Jane", "Doe", "Jane.Doe@berkeley.edu"),
                ("Jane", "Doe", "jane.doe@berkeley.edu"),
            ],
        )

        form = ProvisionCandidatesForm(data={}, files={"file": upload})
        self.assertTrue(form.is_valid(), form.errors)

        form.save()

        self.assertEqual(
            User.objects.filter(username__iexact="jane.doe").count(),
            1,
        )
        self.assertEqual(len(form.email_information), 1)

    def test_duplicate_email_against_existing_user_differing_only_in_case(self):
        # An account already exists with a differently-cased username. A new
        # upload deriving the same username (case-insensitively) should be
        # skipped instead of raising an IntegrityError.
        User.objects.create_user(
            username="John.Smith",
            email="John.Smith@berkeley.edu",
            password="irrelevant",
        )

        upload = _make_csv_upload([("John", "Smith", "john.smith@berkeley.edu")])

        form = ProvisionCandidatesForm(data={}, files={"file": upload})
        self.assertTrue(form.is_valid(), form.errors)

        form.save()

        self.assertEqual(
            User.objects.filter(username__iexact="john.smith").count(),
            1,
        )
        self.assertEqual(len(form.email_information), 0)

    def test_new_candidate_is_still_created_normally(self):
        upload = _make_csv_upload([("Alice", "Nguyen", "alice.nguyen@berkeley.edu")])

        form = ProvisionCandidatesForm(data={}, files={"file": upload})
        self.assertTrue(form.is_valid(), form.errors)

        form.save()

        user = User.objects.get(username="alice.nguyen")
        self.assertEqual(user.email, "alice.nguyen@berkeley.edu")
        self.assertEqual(len(form.email_information), 1)
