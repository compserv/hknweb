from django.urls import path

from . import views

app_name = 'tutoring'
urlpatterns = [
    path(r'', views.index, name='index'),
]
