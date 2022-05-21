from django.urls import path
import hknweb.events.views as views


app_name = "events"

aggregate_display_urls = [
    path("", views.index, name="index"),
    path("rsvps", views.AllRsvpsView.as_view(), name="rsvps"),
    path("leaderboard", views.get_leaderboard, name="leaderboard"),
    path("photos", views.photos, name="photos"),
]

rsvp_transaction_urls = [
    path("<int:id>/rsvp", views.rsvp, name="rsvp"),
    path("<int:id>/unrsvp", views.unrsvp, name="unrsvp"),
    path(
        "<int:id>/confirm_rsvp/<int:operation>", views.confirm_rsvp, name="confirm_rsvp"
    ),
]

event_transaction_urls = [
    path("<int:id>", views.show_details, name="detail"),
    path("new", views.add_event, name="new"),
    path("<int:pk>/edit", views.EventUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete", views.EventDeleteView.as_view(), name="delete"),
]

attendance_urls = [
    path(
        "attendance/<int:event_id>/<int:attendance_form_id>/<int:rsvp_id>",
        views.submit_attendance,
        name="submit_attendance",
    ),
    path(
        "<int:event_id>/attendance/manage",
        views.manage_attendance,
        name="manage_attendance",
    ),
]

urlpatterns = [
    *aggregate_display_urls,
    *rsvp_transaction_urls,
    *event_transaction_urls,
    *attendance_urls,
]
