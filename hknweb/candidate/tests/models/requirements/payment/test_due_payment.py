from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class DuePaymentRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        duepayment = ModelFactory.create_duepayment_requirement(
            candidateSemesterActive=semester,
        )

        self.semester = semester
        self.duepayment = duepayment

    def test_str(self):
        expected = "{} - {}".format(self.duepayment.name, self.semester)
        actual = str(self.duepayment)

        self.assertEqual(expected, actual)
