from django.test import TestCase

from tests.academics.utils import ModelFactory


class RatingModelTests(TestCase):
    def setUp(self):
        rating = ModelFactory.create_default_rating()

        self.rating = rating

    def test_basic(self):
        pass
