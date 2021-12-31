from django.urls import path

import hknweb.course_surveys.views as views


app_name = "course_surveys"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("upload", views.UploadView.as_view(), name="upload"),
]
