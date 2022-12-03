from django.test import TestCase

from tests.candidate.models.utils import ModelFactory


class LogisticsModelTests(TestCase):
    def setUp(self):
        logistics = ModelFactory.create_default_logistics()

        self.logistics = logistics

    def test_populate(self):
        self.logistics.populate(ModelFactory.create_user(username="test_candidate"))

    def test_str(self):
        str(ModelFactory.create_default_event_req())
        str(ModelFactory.create_form_req())
        str(ModelFactory.create_misc_req())
