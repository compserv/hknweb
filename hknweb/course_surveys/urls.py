from django.urls import path

import hknweb.course_surveys.views as views


app_name = "course_surveys"
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"), # @nocommit(rahularya) - need to investigate this more
    path("upload", views.UploadView.as_view(), name="upload"),
    path("upload_csv", views.upload_csv, name="upload_csv"),
    path("merge/questions", views.merge_questions, name="merge_questions"),
    path("merge/instructors", views.merge_instructors, name="merge_instructors"),
]
