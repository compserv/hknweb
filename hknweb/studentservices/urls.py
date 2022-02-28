from django.urls import path

import hknweb.studentservices.views as views


app_name = "studentservices"
urlpatterns = [
    path("resume", views.resume_critique_submit, name="resume"),
    path("resume/submitted", views.resume_critique_uploaded),
]
