from rest_framework import viewsets

from ..permissions import HasPermissionOrReadOnly


class AcademicEntityViewSet(viewsets.ModelViewSet):
    """
    A base viewset class that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.

    See https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
    """
    permission_classes = (HasPermissionOrReadOnly,)
