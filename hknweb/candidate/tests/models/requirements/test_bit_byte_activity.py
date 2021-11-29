from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class BitByteActivityRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        bitbyteactivity_requirement = ModelFactory.create_bitbyteactivity_requirement(
            candidateSemesterActive=semester,
        )

        self.semester = semester
        self.bitbyteactivity_requirement = bitbyteactivity_requirement

    def test_str(self):
        expected = "{} - Number Required: {}{}".format(
            self.semester,
            self.bitbyteactivity_requirement.numberRequired,
            "" if self.bitbyteactivity_requirement.enable else " [Off]",
        )
        actual = str(self.bitbyteactivity_requirement)

        self.assertEqual(expected, actual)
