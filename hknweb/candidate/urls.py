from django.urls import path

import hknweb.candidate.views as views

app_name = "candidate"
urlpatterns = [
    # Portals
    path("", views.candidate_portal, name="candidate_portal"),
    path("portal/<username>", views.candidate_portal_view_by_username, name="candidate_portal_view_by_username"),
    path("officer", views.officer_portal, name="officer_portal"),

    # Form requests
    path("challenge/request", views.request_challenge, name="request_challenge"),
    path("bitbyte/request", views.request_bitbyte, name="request_bitbyte"),

    # Confirm requests
    path("challenge/confirm/<int:pk>/<int:action>", views.confirm_challenge, name="confirm_challenge"),
    path("bitbyte/confirm/<int:pk>/<int:action>", views.confirm_challenge, name="confirm_bitbyte"),

    # Autocomplete
    path(
        "autocomplete/officer",
        views.OfficerAutocomplete.as_view(),
        name="autocomplete_officer",
    ),
    path(
        "autocomplete/user",
        views.UserAutocomplete.as_view(),
        name="autocomplete_user",
    ),
]
