from django.urls import path

import hknweb.studentservices.views as views


app_name = "studentservices"
urlpatterns = [
    path("resume", views.resume_critique_submit, name="resume"),
    path("reviewsessions", views.reviewsessions, name="reviewsessions"),
    path("reviewsessions/<int:id>", views.reviewsession_details),
    path("reviewsessions/new", views.add_reviewsession),
    path(
        "reviewsessions/<int:pk>/edit",
        views.ReviewSessionUpdateView.as_view(),
        name="reviewsession_edit",
    ),
    path("tours", views.tours, name="tours"),
    path("course_guide", views.course_guide, name="course_guide"),
    path("course_guide_data", views.course_guide_data, name="course_guide_data"),
]
