from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Instructor

from hknweb.academics.serializers import InstructorSerializer


class InstructorViewSet(AcademicEntityViewSet):
    queryset = Instructor.objects.order_by("-id")
    serializer_class = InstructorSerializer
