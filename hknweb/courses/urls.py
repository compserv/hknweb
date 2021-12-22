from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("<str:department>/<str:course_number>", views.courses),
    path("addCourse", views.addCourse),
]
