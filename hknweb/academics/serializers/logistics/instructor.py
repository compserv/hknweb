from rest_framework import serializers

from hknweb.academics.models import Instructor


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ["url", "instructor_id"]
        extra_kwargs = {
            "url": {"view_name": "academics:instructor-detail"},
        }
