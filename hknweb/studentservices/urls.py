from django.urls import path

import hknweb.studentservices.views as views


app_name = "studentservices"
urlpatterns = [
    path("resume", views.resume_critique_submit, name="resume"),
    path("resume/submitted", views.resume_critique_uploaded),
    path("reviewsessions", views.reviewsessions, name="reviewsessions"),
    path("reviewsessions/<int:id>", views.reviewsession_details),
    path("reviewsessions/new", views.add_reviewsession),
    path("reviewsessions/<int:pk>/edit", views.ReviewSessionUpdateView.as_view(), name="reviewsession_edit"),
]
