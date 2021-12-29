from rest_framework import permissions


class HasPermissionOrReadOnly(permissions.DjangoModelPermissionsOrAnonReadOnly):
    """
    For coarse-grained, see https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    For fine-grained, see https://www.django-rest-framework.org/api-guide/permissions/#djangoobjectpermissions
    !TODO Implement permissions
    """

    def has_permission(self, request, view):
        """
        Currently, only HKN officers are allowed to view course surveys data through the API.
        This means that API access is purely HKN internal.
        """
        return request.user.groups.filter(name="officer").exists()
