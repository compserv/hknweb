from rest_framework import serializers

from hknweb.academics.models import Survey, ICSR
from hknweb.academics.serializers.course_surveys.rating import RatingSerializer


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    survey_icsr = serializers.HyperlinkedRelatedField(
        view_name="academics:icsr-detail", queryset=ICSR.objects.all()
    )
    rating_survey = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = [
            "url",
            "id",
            "survey_icsr",
            "num_students",
            "response_count",
            "is_private",
            "rating_survey",
        ]
        extra_kwargs = {
            "url": {"view_name": "academics:survey-detail"},
        }
