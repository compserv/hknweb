from rest_framework import serializers

from hknweb.academics.models import Course


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ["url", "id"]
        extra_kwargs = {
            "url": {"view_name": "academics:course-detail"},
        }
