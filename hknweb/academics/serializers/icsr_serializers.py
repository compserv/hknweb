from rest_framework import serializers

from ..models.icsr import ICSR
from ..models.logistics import Course, Department, Instructor, Semester

class ICSRSerializer(serializers.HyperlinkedModelSerializer):
    icsr_course = serializers.HyperlinkedRelatedField(view_name='academics:course-detail', queryset=Course.objects.all())
    icsr_department = serializers.HyperlinkedRelatedField(view_name='academics:department-detail', queryset=Department.objects.all())
    icsr_instructor = serializers.HyperlinkedRelatedField(view_name='academics:instructor-detail', queryset=Instructor.objects.all())
    icsr_semester = serializers.HyperlinkedRelatedField(view_name='academics:semester-detail', queryset=Semester.objects.all())

    class Meta:
        model = ICSR
        fields = [
            'url',
            'id',
            'icsr_course',
            'icsr_department',
            'icsr_instructor',
            'icsr_semester',
            'first_name',
            'last_name',
            'course_number',
            'section_type',
            'section_number',
            'instructor_type',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:icsr-detail'},
        }
