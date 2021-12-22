from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Survey

from hknweb.academics.serializers import SurveySerializer


class SurveyViewSet(AcademicEntityViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
