from django.conf.urls import url

from . import views

app_name = 'alumni'
urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^form/$', views.FormView.as_view(), name='form'),
]