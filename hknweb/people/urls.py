from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^officers/$', views.officers, name='officers'),
    url(r'^cmembers/$', views.committee_members, name='cmembers'),
    url(r'^members/$', views.members, name='members'),
    url(r'^candidates/$', views.candidates, name='candidates'),
    url(r'^election/$', views.election, name='election'), 
    url(r'^contact/$', views.contact, name='contact'),
]
