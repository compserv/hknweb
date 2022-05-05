from django.test import TestCase

from hknweb.candidate.tests.models.utils import ModelFactory


class LogisticsModelTests(TestCase):
    def setUp(self):
        logistics = ModelFactory.create_default_logistics()

        self.logistics = logistics

    def test_populate(self):
        self.logistics.populate(ModelFactory.create_user(username="test_candidate"))
