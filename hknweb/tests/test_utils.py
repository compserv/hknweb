from django.test import TestCase
from django.utils import timezone

from hknweb.utils import get_rand_photo, get_semester_bounds, view_url


class UtilsTests(TestCase):
    def test_get_rand_photo_doesnt_fail(self):
        get_rand_photo()

    def test_view_url_misc_link(self):
        url = "test_url"
        self.assertEqual(view_url(url), url)

    def test_view_url_drive_link(self):
        url = "https://drive.google.com/file/d/(.*)/view?usp=sharing"
        self.assertTrue(view_url(url).startswith("https://drive.google.com/uc?export=view&id="))

    def test_view_url_flickr_link(self):
        url = "https://live.staticflickr.com/(.*)/(.*).jpg"
        self.assertTrue(view_url(url).startswith("https://live.staticflickr.com"))

    def test_get_semester_bounds(self):
        now = timezone.now()

        date = now.replace(month=6)
        get_semester_bounds(date)

        date = now.replace(month=7)
        get_semester_bounds(date)
