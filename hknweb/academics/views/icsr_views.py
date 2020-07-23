from rest_framework import viewsets

from ..permissions import HasPermissionOrReadOnly

from ..models.icsr import ICSR

from ..serializers.icsr_serializers import ICSRSerializer


class ICSRViewSet(viewsets.ModelViewSet):
    queryset = ICSR.objects.all()
    serializer_class = ICSRSerializer
    permission_classes = (HasPermissionOrReadOnly,)
