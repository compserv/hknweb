from django.test import TestCase

from django.urls import reverse

from hknweb.course_surveys.tests.utils import (
    create_user_with_course_surveys_edit_permission,
)


class IndexViewTests(TestCase):
    def setUp(self):
        create_user_with_course_surveys_edit_permission(self)

    def test_returns_200(self):
        response = self.client.get(reverse("course_surveys:index"))

        self.assertEqual(response.status_code, 200)
