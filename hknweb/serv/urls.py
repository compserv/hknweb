from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("eecsday", views.eecsday),
    path("jreecs", views.jreecs),
    path("bearhacks", views.bearhacks),
    path("makershops", views.maker),
    path("calday", views.calday),
]
