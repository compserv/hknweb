from django.urls import path
from . import views

app_name = 'reviewsessions'
urlpatterns = [
    path(r'<int:id>', views.show_details, name='detail'),
    path(r'<int:id>/rsvp', views.rsvp, name='rsvp'),
    path(r'<int:id>/unrsvp', views.unrsvp, name='unrsvp'),
    path('new', views.add_event),
    path(r'<int:pk>/edit', views.EventUpdateView.as_view(), name='edit'),
    path(r'', views.index, name='index'),
]
