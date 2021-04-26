from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('first_name=<str:first_name>&last_name=<str:last_name>/', views.results, name='results'),
]