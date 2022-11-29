from django.test import TestCase

from tests.academics.utils import ModelFactory


class SemesterModelTests(TestCase):
    def setUp(self):
        semester = ModelFactory.create_semester()

        self.semester = semester

    def test_basic(self):
        pass
