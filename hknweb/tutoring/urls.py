from django.urls import path

from hknweb import settings
from django.utils.decorators import method_decorator
from hknweb.utils import login_and_committee

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
    path("portal", views.tutoringportal, name="tutoring_portal"),
    path("courses", views.courses, name="courses"),
    path(
        "crib",
        method_decorator(login_and_committee(settings.TUTORING_GROUP), name="dispatch")(
            views.CribView.as_view()
        ),
        name="crib",
    ),
    path("crib/toggle_public/<int:pk>", views.toggle_public, name="toggle_public"),
]
