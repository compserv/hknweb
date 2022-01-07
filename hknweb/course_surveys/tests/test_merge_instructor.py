import json

from django.test import TestCase

from django.urls import reverse

from hknweb.academics.models import Instructor, ICSR
from hknweb.academics.tests.utils import ModelFactory

from hknweb.course_surveys.constants import Attr
from hknweb.course_surveys.tests.utils import (
    create_user_with_course_surveys_edit_permission,
)


class MergeInstructorViewTests(TestCase):
    def setUp(self):
        create_user_with_course_surveys_edit_permission(self)

    def test_returns_200(self):
        N = 5
        instructors = [ModelFactory.create_instructor(str(i)) for i in range(N)]
        for i in instructors:
            ModelFactory.create_icsr(
                icsr_course=ModelFactory.create_course(),
                icsr_department=ModelFactory.create_department(),
                icsr_instructor=i,
                icsr_semester=ModelFactory.create_semester(),
            )

        self.assertTrue(Instructor.objects.count() == ICSR.objects.count() == N)

        instructor_ids = [str(i.instructor_id) for i in instructors]
        instructor_ids_json = json.dumps(instructor_ids)
        base_url = reverse("course_surveys:merge_instructors")
        url = base_url + "?" + Attr.INSTRUCTOR_IDS + "=" + instructor_ids_json
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Instructor.objects.count(), 1)
        self.assertEqual(ICSR.objects.count(), N)
