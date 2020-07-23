from .base_views import AcademicEntityViewSet

from ..models.icsr import ICSR

from ..serializers.icsr_serializers import ICSRSerializer


class ICSRViewSet(AcademicEntityViewSet):
    queryset = ICSR.objects.all()
    serializer_class = ICSRSerializer
