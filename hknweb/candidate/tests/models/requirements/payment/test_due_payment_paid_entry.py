from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class DuePaymentPaidEntryRequirementModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester(
            semester="Spring",
            year=0,
        )
        duepayment = ModelFactory.create_duepayment_requirement(
            candidateSemesterActive=semester,
        )
        duepaymentpaidentry = ModelFactory.create_duepaymentpaidentry_requirement(
            duePayment=duepayment,
        )

        self.semester = semester
        self.duepayment = duepayment
        self.duepaymentpaidentry = duepaymentpaidentry

    def test_str(self):
        expected = "Payments for: {}".format(self.duepayment)
        actual = str(self.duepaymentpaidentry)

        self.assertEqual(expected, actual)
