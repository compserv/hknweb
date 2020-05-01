from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('<int:id>', views.show_details, name='detail'),
    path('<int:id>/rsvp', views.rsvp, name='rsvp'),
    path('<int:id>/unrsvp', views.unrsvp, name='unrsvp'),
    path('new', views.add_event, name='new'),
    path('<int:pk>/edit', views.EventUpdateView.as_view(), name='edit'),
    path('rsvps', views.AllRsvpsView.as_view(), name='rsvps'),
    path('', views.index, name='index'),
]
