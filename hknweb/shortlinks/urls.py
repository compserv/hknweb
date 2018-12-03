from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('<slug:temp>/', views.openLink),
    path('', views.index, name='index'),

]

