from django.test import TestCase
from hknweb.candidate.models.announcement import Announcement

from tests.candidate.models.utils import ModelFactory


class AnnouncementModelTests(TestCase):
    def setUp(self):
        announcement = ModelFactory.create_announcement()

        self.announcement = announcement

    def test_str_with_title(self):
        expected = self.announcement.title
        actual = str(self.announcement)

        self.assertEqual(expected, actual)

    def test_str_without_title(self):
        self.announcement.title = ""
        self.announcement.save()
        self.announcement = Announcement.objects.get(id=self.announcement.id)

        expected = self.announcement.text
        actual = str(self.announcement)

        self.assertEqual(expected, actual)
