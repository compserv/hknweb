from django.test import TestCase


class ViewSetTests(TestCase):
    def test_basic(self):
        from hknweb.academics.views import (
            QuestionViewSet,
            RatingViewSet,
            SurveyViewSet,
            CourseViewSet,
            DepartmentViewSet,
            InstructorViewSet,
            SemesterViewSet,
            ICSRViewSet,
        )
