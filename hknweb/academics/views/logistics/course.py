from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Course

from hknweb.academics.serializers import CourseSerializer


class CourseViewSet(AcademicEntityViewSet):
    queryset = Course.objects.order_by("-id")
    serializer_class = CourseSerializer
