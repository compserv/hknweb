from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Semester

from hknweb.academics.serializers import SemesterSerializer


class SemesterViewSet(AcademicEntityViewSet):
    queryset = Semester.objects.order_by("-id")
    serializer_class = SemesterSerializer
