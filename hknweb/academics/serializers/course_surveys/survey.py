from rest_framework import serializers

from hknweb.academics.models import Survey, ICSR


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    survey_icsr = serializers.HyperlinkedRelatedField(
        view_name="academics:icsr-detail", queryset=ICSR.objects.all()
    )

    class Meta:
        model = Survey
        fields = [
            "url",
            "id",
            "survey_icsr",
            "num_students",
            "response_count",
            "is_private",
        ]
        extra_kwargs = {
            "url": {"view_name": "academics:survey-detail"},
        }
