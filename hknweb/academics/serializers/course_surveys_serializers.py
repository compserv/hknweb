from rest_framework import serializers

from ..models.course_surveys import Question, Rating, Survey


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating_question', 'rating_survey', 'question_text', 'inverted', 'range_max', 'rating_value']


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'survey_icsr', 'num_students', 'response_count', 'is_private']
