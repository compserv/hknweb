from rest_framework import serializers

from hknweb.academics.models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ["url", "id"]
        extra_kwargs = {
            "url": {"view_name": "academics:question-detail"},
        }
