from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import register_viewsets


app_name = 'academics'

router = DefaultRouter()
register_viewsets(router)

urlpatterns = [
    path('', include(router.urls)),
]
