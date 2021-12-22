from django.test import TestCase

from hknweb.academics.tests.utils import ModelFactory


class SemesterModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester()

        self.semester = semester

    def test_basic(self):
        pass
