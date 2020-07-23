from .base_views import AcademicEntityViewSet

from ..models.course_surveys import Question, Rating, Survey

from ..serializers.course_surveys_serializers import QuestionSerializer, RatingSerializer, SurveySerializer


class QuestionViewSet(AcademicEntityViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class RatingViewSet(AcademicEntityViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class SurveyViewSet(AcademicEntityViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
