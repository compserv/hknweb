from django.urls import path
from . import views


urlpatterns = [
    path('academics/departments', views.index),
]