from rest_framework import viewsets

from ..permissions import HasPermissionOrReadOnly


class AcademicEntityViewSet(viewsets.ModelViewSet):
    """
    A base viewset class that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    permission_classes = (HasPermissionOrReadOnly,)
