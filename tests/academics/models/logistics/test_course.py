from django.test import TestCase

from tests.academics.utils import ModelFactory


class CourseModelTests(TestCase):
    def setUp(self):
        course = ModelFactory.create_course()

        self.course = course

    def test_basic(self):
        pass
