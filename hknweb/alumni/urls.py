from django.conf.urls import url

from . import views

app_name = 'alumni'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^form/$', views.form, name='form'),
]