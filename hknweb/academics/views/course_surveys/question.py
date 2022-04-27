from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Question

from hknweb.academics.serializers import QuestionSerializer


class QuestionViewSet(AcademicEntityViewSet):
    queryset = Question.objects.order_by("-id")
    serializer_class = QuestionSerializer
