from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class CandidateFormRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        candidateform = ModelFactory.create_candidateform_requirement(
            candidateSemesterActive=semester,
        )

        self.semester = semester
        self.candidateform = candidateform

    def test_str(self):
        expected = "{} - {}".format(self.candidateform.name, self.semester)
        actual = str(self.candidateform)

        self.assertEqual(expected, actual)
