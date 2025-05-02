from django.urls import path

import hknweb.industry.views as views


app_name = "industry"
urlpatterns = [
    path("what_is_hkn", views.what_is_hkn, name="what_is_hkn"),
    path("resume_book", views.resume_book, name="resume_book"),
    path("eecs_career_fair", views.eecs_career_fair, name="eecs_career_fair"),
    path("infosessions", views.infosessions, name="infosessions"),
    path("current_sponsors", views.current_sponsors, name="current_sponsors"),
]
