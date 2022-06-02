from django.urls import path

from . import views

app_name = "tutoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/slots", views.slots, name="slots"),
]
