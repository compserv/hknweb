from rest_framework import serializers

from ..models.course_surveys import Question, Rating, Survey
from ..models.icsr import ICSR


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['url', 'id', 'current_text',
                  'recent_semester']
        extra_kwargs = {
            'url': {'view_name': 'academics:question-detail'},
        }


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    rating_question = serializers.HyperlinkedRelatedField(view_name='academics:question-detail', queryset=Question.objects.all())
    rating_survey = serializers.HyperlinkedRelatedField(view_name='academics:survey-detail', queryset=Survey.objects.all())

    class Meta:
        model = Rating
        fields = ['url', 'id', 'rating_question', 'rating_survey', 'question_text', 'inverted', 'range_max', 'rating_value']
        extra_kwargs = {
            'url': {'view_name': 'academics:rating-detail'},
        }


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    survey_icsr = serializers.HyperlinkedRelatedField(view_name='academics:icsr-detail', queryset=ICSR.objects.all())

    class Meta:
        model = Survey
        fields = ['url', 'id', 'survey_icsr', 'num_students', 'response_count', 'is_private']
        extra_kwargs = {
            'url': {'view_name': 'academics:survey-detail'},
        }
