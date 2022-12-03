from django.urls import include, path
from rest_framework.routers import APIRootView, DefaultRouter

from .permissions import HasPermissionOrReadOnly
from .views import register_viewsets


app_name = "academics"

router = DefaultRouter()


class RootView(APIRootView):
    permission_classes = [HasPermissionOrReadOnly]


router.APIRootView = RootView

register_viewsets(router)

urlpatterns = [
    path("api/", include(router.urls)),
]
