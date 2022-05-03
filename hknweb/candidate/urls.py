from django.urls import path

import hknweb.candidate.views as views

app_name = "candidate"
urlpatterns = [
    path("", views.candidate_portal, name="candidate_portal"),
    path("portal/<username>", views.candidate_portal_view_by_username, name="viewcand"),
    # candidate end of officer challenge requests
    path("candreq", views.CandRequestView.as_view(), name="candrequests"),
    # officer end of officer challenge requests
    path("officer", views.OfficerPortalView.as_view(), name="officer"),
    path("bitbyte", views.BitByteView.as_view(), name="bitbyte"),
    path(
        "challengeconfirm/<int:pk>/",
        views.officer_confirm_view,
        name="challengeconfirm",
    ),
    path("<int:id>/confirm", views.confirm_challenge, name="confirm"),
    path("detail/<int:pk>/", views.challenge_detail_view, name="detail"),
    path(
        "reviewconfirm/<int:pk>/",
        views.officer_review_confirmation,
        name="reviewconfirm",
    ),
    path(
        "candreq/autocomplete/",
        views.OfficerAutocomplete.as_view(),
        name="candreq/autocomplete",
    ),
    path(
        "bitbyte/autocomplete/",
        views.UserAutocomplete.as_view(),
        name="bitbyte/autocomplete",
    ),
]
