from django.urls import path

import hknweb.candidate.views as views

app_name = "candidate"
urlpatterns = [
    # Portals
    path("", views.candidate_portal, name="candidate_portal"),
    path(
        "portal/<username>",
        views.candidate_portal_view_by_username,
        name="candidate_portal_view_by_username",
    ),
    path("officer", views.officer_portal, name="officer_portal"),
    # Form requests
    path("challenge/request", views.request_challenge, name="request_challenge"),
    path("bitbyte/request", views.request_bitbyte, name="request_bitbyte"),
    # Confirm requests
    path(
        "challenge/confirm/<int:pk>/<int:action>",
        views.confirm_challenge,
        name="confirm_challenge",
    ),
    path(
        "bitbyte/confirm/<int:pk>/<int:action>",
        views.confirm_bitbyte,
        name="confirm_bitbyte",
    ),
    path(
        "checkoff_req",
        views.checkoff_req,
        name="checkoff_req",
    ),
    path(
        "checkoff_event",
        views.checkoff_event,
        name="checkoff_event",
    ),
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
    # Shortlinks
    path(
        "shortlinks",
        views.manage_shortlinks,
        name="manage_shortlinks",
    ),
    path(
        "shortlinks/create",
        views.create_shortlink,
        name="create_shortlink",
    ),
    path(
        "shortlinks/import",
        views.import_shortlinks,
        name="import_shortlinks",
    ),
]
