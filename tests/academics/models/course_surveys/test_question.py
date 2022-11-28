from django.test import TestCase

from tests.academics.utils import ModelFactory


class QuestionModelTests(TestCase):
    def setUp(self):
        question = ModelFactory.create_question()

        self.question = question

    def test_basic(self):
        pass
