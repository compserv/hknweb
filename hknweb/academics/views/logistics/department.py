from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Department

from hknweb.academics.serializers import DepartmentSerializer


class DepartmentViewSet(AcademicEntityViewSet):
    queryset = Department.objects.order_by("-id")
    serializer_class = DepartmentSerializer
