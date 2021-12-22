from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class CommitteeProjectRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        committeeproject = ModelFactory.create_committeeproject_requirement(
            candidateSemesterActive=semester,
        )

        self.semester = semester
        self.committeeproject = committeeproject

    def test_str(self):
        expected = "{} - {}".format(self.committeeproject.name, self.semester)
        actual = str(self.committeeproject)

        self.assertEqual(expected, actual)
