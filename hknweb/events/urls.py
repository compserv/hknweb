from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    # url(r'^calendar/$', views.index),
    path(r'<int:id>', views.show_details),
    path(r'<int:id>/rsvp', views.rsvp),
    path(r'<int:id>/unrsvp', views.unrsvp),
    path(r'', views.index),
    # url(r'^future/$', views.future, name='future'),
    # url(r'^past/$', views.past, name='past'),
    # url(r'^rsvps/$', views.rsvps, name='rsvps'),
]
