from rest_framework import viewsets

from ..permissions import HasPermissionOrReadOnly

from ..models.logistics import Course, Department, Instructor, Semester

from ..serializers.logistics_serializers import (
    CourseSerializer,
    DepartmentSerializer,
    InstructorSerializer,
    SemesterSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (HasPermissionOrReadOnly,)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (HasPermissionOrReadOnly,)


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = (HasPermissionOrReadOnly,)


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = (HasPermissionOrReadOnly,)
