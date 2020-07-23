from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import register_viewsets


app_name = 'academics'

router = DefaultRouter()
register_viewsets(router)

urlpatterns = [
    url(r'^', include(router.urls))
]
