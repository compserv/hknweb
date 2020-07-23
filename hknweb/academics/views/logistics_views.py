from .base_views import AcademicEntityViewSet

from ..models.logistics import Course, Department, Instructor, Semester

from ..serializers.logistics_serializers import (
    CourseSerializer,
    DepartmentSerializer,
    InstructorSerializer,
    SemesterSerializer,
)


class CourseViewSet(AcademicEntityViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DepartmentViewSet(AcademicEntityViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class InstructorViewSet(AcademicEntityViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class SemesterViewSet(AcademicEntityViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
