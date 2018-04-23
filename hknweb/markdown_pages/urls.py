from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.editor),
    url(r'^(?P<path>[\w\d\.\-_]+)/', views.display)
]
