from hknweb.academics.views.base_viewset import AcademicEntityViewSet

from hknweb.academics.models import Rating

from hknweb.academics.serializers import RatingSerializer


class RatingViewSet(AcademicEntityViewSet):
    queryset = Rating.objects.order_by("-id")
    serializer_class = RatingSerializer
