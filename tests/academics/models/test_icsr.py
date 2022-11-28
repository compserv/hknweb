from django.test import TestCase

from tests.academics.utils import ModelFactory


class ICSRModelTests(TestCase):
    def setUp(self):
        icsr = ModelFactory.create_default_icsr()

        self.icsr = icsr

    def test_basic(self):
        pass
