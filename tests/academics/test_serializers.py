from django.test import TestCase


class SerializerTests(TestCase):
    def test_basic(self):
        from hknweb.academics.serializers import (
            QuestionSerializer,
            RatingSerializer,
            SurveySerializer,
            CourseSerializer,
            DepartmentSerializer,
            InstructorSerializer,
            SemesterSerializer,
            ICSRSerializer,
        )
