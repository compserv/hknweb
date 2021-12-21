from rest_framework import serializers

from hknweb.academics.models import Semester


class SemesterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semester
        fields = ["url", "id", "year", "year_section"]
        extra_kwargs = {
            "url": {"view_name": "academics:semester-detail"},
        }
