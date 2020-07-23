from rest_framework import permissions, viewsets

from ..permissions import HasPermissionOrReadOnly

from ..models.course_surveys import Question, Rating, Survey

from ..serializers.course_surveys_serializers import QuestionSerializer, RatingSerializer, SurveySerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasPermissionOrReadOnly,)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasPermissionOrReadOnly,)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasPermissionOrReadOnly,)