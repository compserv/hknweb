from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class MandatoryRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        mandatory_requirement = ModelFactory.create_mandatory_requirement(
            candidateSemesterActive=semester,
        )

        self.semester = semester
        self.mandatory_requirement = mandatory_requirement

    def test_str(self):
        expected = "{} Mandatory - {} to {}{}".format(
            self.semester,
            self.mandatory_requirement.eventsDateStart,
            self.mandatory_requirement.eventsDateEnd,
            " [Off]",
        )
        actual = str(self.mandatory_requirement)

        self.assertEqual(expected, actual)
