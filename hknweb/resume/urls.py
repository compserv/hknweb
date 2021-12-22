from django.urls import path

import hknweb.resume.views as views


app_name = "resume"
urlpatterns = [
    path("", views.index, name="index"),
    path("submitted", views.submitted),
]
