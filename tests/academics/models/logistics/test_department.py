from django.test import TestCase

from tests.academics.utils import ModelFactory


class DepartmentModelTests(TestCase):
    def setUp(self):
        department = ModelFactory.create_department()

        self.department = department

    def test_basic(self):
        pass
