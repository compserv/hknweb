from django.conf.urls import url

from . import views

app_name = 'alumni'
urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^form/$', views.FormView, name='form'),
    url(r'^form_success/$', views.FormViewSuccess, name='form_success')
]
