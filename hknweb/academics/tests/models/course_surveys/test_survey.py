from django.test import TestCase

from hknweb.academics.tests.utils import ModelFactory


class SurveyModelTests(TestCase):
    def setUp(self):
        survey = ModelFactory.create_default_survey()

        self.survey = survey

    def test_basic(self):
        pass
