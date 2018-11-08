from django.urls import path

from . import views

app_name = 'alumni'
urlpatterns = [
    path(r'^form_success/$', views.FormViewSuccess, name='form_success'),
    path(r'^$', views.IndexView.as_view()),
    path(r'^form/$', views.FormView, name='form'),
]
