from rest_framework import viewsets

from ..permissions import HasPermissionOrReadOnly


class AcademicEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (HasPermissionOrReadOnly,)
