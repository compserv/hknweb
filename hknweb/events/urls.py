from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^calendar/$', views.index),
    url(r'^future/$', views.future, name='future'),
    url(r'^past/$', views.past, name='past'),
    url(r'^rsvps/$', views.rsvps, name='rsvps'),
]
