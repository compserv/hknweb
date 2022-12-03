from django.test import TestCase

from tests.academics.utils import ModelFactory


class SurveyModelTests(TestCase):
    def setUp(self):
        survey = ModelFactory.create_default_survey()

        self.survey = survey

    def test_basic(self):
        pass
