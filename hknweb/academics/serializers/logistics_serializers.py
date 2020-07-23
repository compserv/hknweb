from rest_framework import serializers

from ..models.logistics import Course, Department, Instructor, Semester


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'abbr']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['instructor_id']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'year', 'year_section']
