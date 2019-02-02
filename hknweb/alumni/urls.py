from django.urls import path

from . import views

app_name = 'alumni'
urlpatterns = [
    # When doing the officer challenge feature, I changed all these from
    # re_path to path
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('detail/(?P<oid>\d+)/', views.alumni_detail_view, name='detail'),
    path('search_type/', views.search_type, name='search_type'),
    path('form/', views.form, name='form'),
]
