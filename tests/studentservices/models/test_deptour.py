from django.test import TestCase

from django.utils import timezone

from hknweb.studentservices.models import DepTour


class CourseGuideModelTests(TestCase):
    def test_course_guide_models(self):
        deptour = DepTour.objects.create(datetime=timezone.now())

        self.assertTrue(repr(deptour))
