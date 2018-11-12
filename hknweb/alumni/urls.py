from django.urls import re_path

from . import views

app_name = 'alumni'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^search/$', views.SearchView.as_view(), name='search'),
    re_path(r'^detail/(?P<oid>\d+)/$', views.alumni_detail_view, name='detail'),
    re_path(r'^search_type/$', views.search_type, name='search_type'),
    re_path(r'^form/$', views.form, name='form'),
    re_path(r'^form_success/$', views.form_success, name='form_success'),
]
