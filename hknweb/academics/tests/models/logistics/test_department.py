from django.test import TestCase

from hknweb.academics.tests.utils import ModelFactory


class DepartmentModelTests(TestCase):
    def setUp(self):
        department = ModelFactory.create_department()

        self.department = department

    def test_basic(self):
        pass
