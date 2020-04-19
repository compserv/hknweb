from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
	path('course/<department>/<number>/', views.exams_for_course),
    path('new', views.add_exam),
    url(r'^$', views.index),
]