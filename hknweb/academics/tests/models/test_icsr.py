from django.test import TestCase

from hknweb.academics.tests.utils import ModelFactory


class ICSRModelTests(TestCase):
    def setUp(self):
        icsr = ModelFactory.create_default_icsr()

        self.icsr = icsr

    def test_basic(self):
        pass
