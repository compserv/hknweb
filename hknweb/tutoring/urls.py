from django.urls import path

from . import views

app_name = "tutoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/slots", views.slots, name="slots"),
    path(
        "autocomplete/course",
        views.course_autocomplete,
        name="autocomplete_course",
    ),
    path(
        "autocomplete/tutor",
        views.tutor_autocomplete,
        name="autocomplete_tutor",
    ),
]
