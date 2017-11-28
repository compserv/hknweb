from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^future/$', views.future, name='future'),
    url(r'^past/$', views.past, name='past'),
    url(r'^rsvps/$', views.rsvps, name='rsvps'),
]
