from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'<int:id>', views.show_details),
    path(r'<int:id>/rsvp', views.rsvp),
    path(r'<int:id>/unrsvp', views.unrsvp),
    path(r'', views.index),
]
