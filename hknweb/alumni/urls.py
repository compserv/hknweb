from django.urls import re_path

from . import views

app_name = 'alumni'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^search/$', views.SearchView.as_view(), name='search'),
    re_path(r'^form/$', views.FormView, name='form'),
    re_path(r'^form_success/$', views.FormViewSuccess, name='form_success'),
]
