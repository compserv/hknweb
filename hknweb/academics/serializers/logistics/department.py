from rest_framework import serializers

from hknweb.academics.models import Department


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ["url", "id", "name", "abbr"]
        extra_kwargs = {
            "url": {"view_name": "academics:department-detail"},
        }
