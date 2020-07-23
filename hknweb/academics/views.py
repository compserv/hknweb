from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import HasPermissionOrReadOnly

from .models.course_surveys import Question, Rating, Survey
from .models.icsr import ICSR
from .models.logistics import Course, Department, Instructor, Semester

from .serializers.course_surveys_serializers import QuestionSerializer, RatingSerializer, SurveySerializer
from .serializers.icsr_serializers import ICSRSerializer
from.serializers.logistics_serializers import (
    CourseSerializer,
    DepartmentSerializer,
    InstructorSerializer,
    SemesterSerializer,
)
