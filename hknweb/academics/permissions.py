from rest_framework import permissions


class HasPermissionOrReadOnly(permissions.DjangoModelPermissionsOrAnonReadOnly):
    """
    For coarse-grained, see https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    For fine-grained, see https://www.django-rest-framework.org/api-guide/permissions/#djangoobjectpermissions
    !TODO Implement permissions
    """

    pass
