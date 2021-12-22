from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class HangoutRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        hangout_requirement = ModelFactory.create_hangout_requirement(
            candidateSemesterActive=semester,
        )

        self.semester = semester
        self.hangout_requirement = hangout_requirement

    def test_str(self):
        expected = "{} {} - Number Required: {}{}".format(
            self.semester,
            self.hangout_requirement.eventType,
            self.hangout_requirement.numberRequired,
            " [Off]",
        )
        actual = str(self.hangout_requirement)

        self.assertEqual(expected, actual)
