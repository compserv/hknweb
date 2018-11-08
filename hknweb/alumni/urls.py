from django.conf.urls import url

from . import views

app_name = 'alumni'
urlpatterns = [
    path(r'^$', views.IndexView.as_view()),
    path(r'^form/$', views.FormView, name='form'),
]
