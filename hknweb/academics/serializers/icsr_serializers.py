from rest_framework import serializers

from ..models.icsr import ICSR


class ICSRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICSR
        fields = [
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
