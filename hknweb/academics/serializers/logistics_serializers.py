from rest_framework import serializers

from ..models.logistics import Course, Department, Instructor, Semester


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['url', 'id','current_name']
        extra_kwargs = {
            'url': {'view_name': 'academics:course-detail'},
        }


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['url', 'id', 'name', 'abbr']
        extra_kwargs = {
            'url': {'view_name': 'academics:department-detail'},
        }


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ['url', 'instructor_id','current_first_name', 'current_last_name', 'current_instructor_type']
        extra_kwargs = {
            'url': {'view_name': 'academics:instructor-detail'},
        }


class SemesterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semester
        fields = ['url', 'id', 'year', 'year_section']
        extra_kwargs = {
            'url': {'view_name': 'academics:semester-detail'},
        }
