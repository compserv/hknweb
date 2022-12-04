from django.test import TestCase

from hknweb.candidate.templatetags.app_filters import is_link


class AppFiltersTests(TestCase):
    def test_is_link(self):
        self.assertTrue(is_link("https://www.google.com/"))
        self.assertFalse(is_link("not a link"))
