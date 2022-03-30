from django.urls import path
from django.urls import re_path

from . import views


app_name = "pages"
urlpatterns = [
    # @nocommit: why is this even a thing?
    # path("", views.editor),
    # re_path(r"^(?P<path>[\w\d\.\-_]+)/", views.display),
]
