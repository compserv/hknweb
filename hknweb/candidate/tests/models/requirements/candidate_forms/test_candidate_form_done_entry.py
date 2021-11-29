from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class CandidateFormDoneEntryRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        candidateform = ModelFactory.create_candidateform_requirement(
            candidateSemesterActive=semester,
        )
        candidateformdoneentry = ModelFactory.create_candidateformdoneentry_requirement(
            form=candidateform,
        )

        self.semester = semester
        self.candidateform = candidateform
        self.candidateformdoneentry = candidateformdoneentry

    def test_str(self):
        expected = "Forms filled for: {}".format(self.candidateform)
        actual = str(self.candidateformdoneentry)

        self.assertEqual(expected, actual)
