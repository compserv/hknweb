from django.test import TestCase

from hknweb.academics.tests.utils import ModelFactory


class RatingModelTests(TestCase):
    def setUp(self):
        rating = ModelFactory.create_default_rating()

        self.rating = rating

    def test_basic(self):
        pass
