from django.test import TestCase

from django.urls import reverse

from hknweb.course_surveys.tests.utils import (
    create_user_with_course_surveys_edit_permission,
    ModelFactory,
)
from hknweb.markdown_pages.models import MarkdownPage


class IndexViewTests(TestCase):
    def setUp(self):
        create_user_with_course_surveys_edit_permission(self)

    def test_returns_200(self):
        response = self.client.get(reverse("course_surveys:index"))

        self.assertEqual(response.status_code, 200)

    def test_cas_signed_in_returns_200(self):
        s = self.client.session
        s["signed_in"] = True
        s.save()

        ModelFactory.create_default_rating()

        response = self.client.get(reverse("course_surveys:index"))

        self.assertEqual(response.status_code, 200)

    def test_search_by_instructors_returns_200(self):
        s = self.client.session
        s["signed_in"] = True
        s.save()

        ModelFactory.create_default_rating()

        response = self.client.get(
            reverse("course_surveys:index") + "?search_by=instructors"
        )

        self.assertEqual(response.status_code, 200)

    def test_course_id_present_returns_200(self):
        s = self.client.session
        s["signed_in"] = True
        s.save()

        rating = ModelFactory.create_default_rating()

        response = self.client.get(
            reverse("course_surveys:index")
            + f"?course={rating.rating_survey.survey_icsr.icsr_course.id}"
        )

        self.assertEqual(response.status_code, 200)

    def test_instructor_id_present_returns_200(self):
        s = self.client.session
        s["signed_in"] = True
        s.save()

        rating = ModelFactory.create_default_rating()
        rating.rating_survey.survey_icsr.is_private = False
        rating.rating_survey.survey_icsr.save()

        response = self.client.get(
            reverse("course_surveys:index")
            + f"?instructor={rating.rating_survey.survey_icsr.icsr_instructor.instructor_id}"
        )

        self.assertEqual(response.status_code, 200)

    def test_instructor_id_present_returns_200(self):
        s = self.client.session
        s["signed_in"] = True
        s.save()

        MarkdownPage.objects.create(
            name="test_name",
            path="course_surveys_authentication",
            description="test_description",
            body="test_body",
        )

        response = self.client.get(reverse("course_surveys:index"))

        self.assertEqual(response.status_code, 200)
