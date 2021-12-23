from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import ICSR

from hknweb.academics.serializers import ICSRSerializer


class ICSRViewSet(AcademicEntityViewSet):
    queryset = ICSR.objects.all()
    serializer_class = ICSRSerializer
