from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class CommitteeProjectDoneEntryRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        committeeproject = ModelFactory.create_committeeproject_requirement(
            candidateSemesterActive=semester,
        )
        committeeprojectdoneentry = ModelFactory.create_committeeprojectdoneentry_requirement(
            committeeProject=committeeproject,
        )

        self.semester = semester
        self.committeeproject = committeeproject
        self.committeeprojectdoneentry = committeeprojectdoneentry

    def test_str(self):
        expected = "Committee Project completed for: {}".format(self.committeeproject)
        actual = str(self.committeeprojectdoneentry)

        self.assertEqual(expected, actual)
