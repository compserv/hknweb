from rest_framework import serializers

from hknweb.academics.models import Question, Rating, Survey


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    rating_question = serializers.HyperlinkedRelatedField(
        view_name="academics:question-detail", queryset=Question.objects.all()
    )
    rating_survey = serializers.HyperlinkedRelatedField(
        view_name="academics:survey-detail", queryset=Survey.objects.all()
    )

    class Meta:
        model = Rating
        fields = [
            "url",
            "id",
            "rating_question",
            "rating_survey",
            "question_text",
            "inverted",
            "range_max",
            "rating_value",
        ]
        extra_kwargs = {
            "url": {"view_name": "academics:rating-detail"},
        }
