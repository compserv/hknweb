from django.test import TestCase

from tests.academics.utils import ModelFactory


class InstructorModelTests(TestCase):
    def setUp(self):
        instructor_id = "my instructor id"
        instructor = ModelFactory.create_instructor(instructor_id)

        self.instructor = instructor

    def test_basic(self):
        pass
